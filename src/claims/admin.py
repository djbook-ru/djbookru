# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _
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

class ClaimsAdmin(admin.ModelAdmin):
    form = ClaimsAdminForm
    fieldsets = (
        (_(u'Meta'),
         {'fields': ('datetime', 'url', 'status')}),
        (_(u'Error'),
         {'fields': ('ctx_left', 'selected', 'ctx_right')}),
        (_(u'Comment'),
         {'fields': ('email','comment')})
        )
    list_display = ('url', 'comment', 'email', 'notify',
                    claim_status_field, 'datetime')
    ordered = ('-datetime')

admin.site.register(Claims, ClaimsAdmin)