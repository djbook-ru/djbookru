# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _
from django.db.models.aggregates import Max
from claims.models import Claims, ClaimStatus, CLAIM_STATUSES

class ClaimsAdminForm(forms.ModelForm):
    """ Класс отображения формы, расширяем функционал модели Claims. """
    status = forms.ChoiceField(choices=CLAIM_STATUSES)

    def __init__(self, *args, **kwargs):
        super(ClaimsAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['status'].initial = self.instance.get_status()

    def save(self, *args, **kwargs):
        d = self.cleaned_data
        m = super(ClaimsAdminForm, self).save(*args, **kwargs)
        if m and d.get('status'):
            m.set_status(d.get('status'))
        return m

    class Meta:
        model = Claims

def get_choice_desc(code):
    """ Функция возвращает описание по коду. См. CHOICES. """
    #logging.debug(filter(lambda x, c=code: x[0]==c, list(CLAIM_STATUSES)))
    return CLAIM_STATUSES[int(code)-1][1]

# additional field: claim status
def claim_status_field(claim):
    try:
        code = ClaimStatus.objects.filter(claim=claim).order_by('-applied')[0].status
    except Exception:
        return _(u'Unknown')
    color = ['yellow', 'orange', 'green', 'red'][int(code)-1]
    return '<div style="background-color: %s; padding: 2px 3px; text-align: center">%s</div>' \
        % (color, unicode(get_choice_desc(code)))
claim_status_field.short_description = _(u'Claim status')
claim_status_field.allow_tags = True

ASSIGNED = '2'
FIXED = '3'
INVALID = '4'

def make_assigned(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for item in Claims.objects.filter(id__in=selected).all():
        item.set_status(ASSIGNED)
make_assigned.short_description = _("Mark selected claims as assigned")

def make_fixed(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for item in Claims.objects.filter(id__in=selected).all():
        item.set_status(FIXED)
make_fixed.short_description = _("Mark selected claims as fixed")

def make_invalid(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for item in Claims.objects.filter(id__in=selected).all():
        item.set_status(INVALID)
make_invalid.short_description = _("Mark selected claims as invalid")

class ClaimsAdmin(admin.ModelAdmin):
    form = ClaimsAdminForm
    fieldsets = (
        (_(u'Meta'),
         {'fields': ('datetime', 'url')}),
        (_(u'Error'),
         {'fields': ('ctx_left', 'selected', 'ctx_right')}),
        (_(u'Comment'),
         {'fields': ('status', 'email','comment')})
        )
    list_display = ('url', 'comment', 'email', 'notify',
                    claim_status_field, 'datetime')
    ordering = ('claimstatus__status__max',)
    actions = [make_assigned, make_fixed, make_invalid]

    def queryset(self, request):
        qs = super(ClaimsAdmin, self).queryset(request)
        return qs.annotate(Max('claimstatus__status'))

admin.site.register(Claims, ClaimsAdmin)

