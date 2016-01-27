# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import mail_managers
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from pagedown.widgets import PagedownWidget

from .models import Jobs


class AddPositionForm(forms.ModelForm):

    class Meta:
        model = Jobs
        fields = ('employment_type', 'location', 'remote_work', 'title',
                  'description', 'company_name', 'company_website',
                  'how_to_apply')

    class Media(object):
        css = {
            'all': ('theme/css/pagedown.css',) # css rules for pagedown widget
        }

    def __init__(self, *args, **kwargs):
        super(AddPositionForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = PagedownWidget()
        self.fields['description'].help_text = _(u'Use markdown')
        self.fields['how_to_apply'].help_text = _(u'For example:'
            ' Email your resume to job@contact.me')

    def save(self, user):
        obj = super(AddPositionForm, self).save(False)
        obj.author = user
        obj.status = obj.PUBLISHED
        obj.save()

        # sending messages to the administrator about adding positions
        subject = _(u'New vacancy has been added on djbook.ru')
        message = _(u'User %(author)s added a new vacancy on djbook.ru.\n\n'
                    'Please check and approve it. URL: %(link)s') % {
            'link': 'http://%s%s' % (Site.objects.get_current().domain, obj.get_edit_url()),
            'author': obj.author}
        mail_managers(subject, message, True)

        return obj


class EditPositionForm(forms.ModelForm):
    # TODO: Inherit from form AddPositionForm

    class Meta:
        model = Jobs
        fields = ('employment_type', 'location', 'remote_work', 'title',
                  'description', 'company_name', 'company_website',
                  'how_to_apply')

    class Media(object):
        css = {
            'all': ('theme/css/pagedown.css',) # css rules for pagedown widget
        }

    def __init__(self, *args, **kwargs):
        super(EditPositionForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = PagedownWidget()
        self.fields['description'].help_text = _(u'Use markdown')
        self.fields['how_to_apply'].help_text = _(u'For example:'
            ' Email your resume to job@contact.me')

    def save(self, user):
        obj = super(EditPositionForm, self).save(False)
        obj.author = user
        obj.status = obj.PUBLISHED
        obj.save()

        return obj
