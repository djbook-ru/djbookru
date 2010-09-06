from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

class FlatpageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))

    class Meta:
        model = FlatPage

class FlatPageAdmin(admin.ModelAdmin):
    form = FlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'enable_comments')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('registration_required', 'template_name')}),
    )
    list_display = ('url', 'title', 'enable_comments')
    list_editable = ('enable_comments',)
    list_filter = ('enable_comments', 'registration_required')
    search_fields = ('url', 'title')
    save_on_top = True
    
    def save_model(self, request, new_object, form, change=False):
        super(FlatPageAdmin, self).save_model(request, new_object, form, change)
        new_object.sites.add(settings.SITE_ID)

def sites_flatpages_patch():
    admin.site.unregister(Site)
    admin.site.unregister(FlatPage)
    admin.site.register(FlatPage, FlatPageAdmin)
