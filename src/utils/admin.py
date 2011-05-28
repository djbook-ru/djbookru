from django.contrib import admin
from django.forms.formsets import all_valid
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import helpers
from django.contrib.admin.util import unquote
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode, smart_unicode
from django.http import Http404
from utils.models import LogEntryExtend
from django.contrib.admin.models import LogEntry, CHANGE
from copy import deepcopy

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('object_repr', 'content_type', 'user', 'change_message', 'action_time')
    list_filter = ('content_type',)
    readonly_fields = ('version',)
    
    def version(self, obj):
        if not obj.more:
            return ''
        
        data_obj = obj.more.data
        
        output = []
        output.append(u'<table>')
        row = u'<tr><td>%s</td><td><pre>%s</pre></td></tr>'
        for f in data_obj._meta.local_fields:
            val = getattr(data_obj, f.get_attname())
            output.append(row % (f.verbose_name, val))
        output.append(u'</table>')
        
        return u''.join(output)
    
    version.allow_tags = True
    
admin.site.register(LogEntry, LogEntryAdmin)

class LogModelAdmin(admin.ModelAdmin):
    
    def log_change(self, request, object, message, old_object=None):
        """
        Log that an object has been successfully changed.

        The default implementation creates an admin LogEntry object.
        """
        entry = LogEntry()
        entry.user = request.user
        entry.content_type = ContentType.objects.get_for_model(object)
        entry.object_id = smart_unicode(object.pk)
        entry.object_repr = force_unicode(object)[:200]
        entry.action_flag = CHANGE
        entry.change_message = message
        entry.save()
        
        if old_object:
            entry_extend = LogEntryExtend()
            entry_extend.entry = entry
            entry_extend.data = old_object
            entry_extend.save()
        
    @admin.options.csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))
        old_object = deepcopy(obj)
        
        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and request.POST.has_key("_saveasnew"):
            return self.add_view(request, form_url='../add/')

        ModelForm = self.get_form(request, obj)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, new_object),
                                       self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(request.POST, request.FILES,
                                  instance=new_object, prefix=prefix,
                                  queryset=inline.queryset(request))

                formsets.append(formset)

            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=True)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=True)

                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message, old_object)
                return self.response_change(request, new_object)

        else:
            form = ModelForm(instance=obj)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, obj), self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
            self.prepopulated_fields, self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': request.REQUEST.has_key('_popup'),
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)    