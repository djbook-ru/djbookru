# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import mail_managers
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from pytils.translit import slugify

from pagedown.widgets import PagedownWidget

from .models import Jobs


class AddPositionForm(forms.ModelForm):

    class Meta:
        model = Jobs
        fields = ('employment_type', 'location', 'remote_work', 'title',
                  'description', 'company_name', 'company_website',
                  'how_to_apply')
        widgets = {
            'description': PagedownWidget(),
        }
        help_texts = {
            'description': _(u'Use markdown'),
            'how_to_apply': _(u'For example: Email your resume to job@contact.me'),
        }

    class Media(object):
        css = {
            'all': ('theme/css/pagedown.css',)  # css rules for pagedown widget
        }

    def save(self, user):
        obj = super(AddPositionForm, self).save(commit=False)
        obj.author = user
        obj.status = obj.PUBLISHED
        obj.company_name_slug = slugify(obj.company_name)
        obj.save()

        # sending messages to the administrator about adding positions
        subject = _(u'New vacancy has been added on djbook.ru')
        message = _(u'User %(author)s added a new vacancy on djbook.ru.\n\n'
                    'Please check and approve it. URL: %(link)s') % {
            'link': 'http://%s%s' % (Site.objects.get_current().domain, obj.get_edit_url()),
            'author': obj.author}
        mail_managers(subject, message, fail_silently=True)

        return obj


class EditPositionForm(forms.ModelForm):
    # TODO: Inherit from form AddPositionForm

    class Meta:
        model = Jobs
        fields = ('employment_type', 'location', 'remote_work', 'title',
                  'description', 'company_name', 'company_website',
                  'how_to_apply')
        widgets = {
            'description': PagedownWidget(),
        }
        help_texts = {
            'description': _(u'Use markdown'),
            'how_to_apply': _(u'For example: Email your resume to job@contact.me'),
        }

    class Media(object):
        css = {
            'all': ('theme/css/pagedown.css',)  # css rules for pagedown widget
        }

    def save(self, user):
        obj = super(EditPositionForm, self).save(commit=False)
        obj.author = user
        obj.status = obj.PUBLISHED
        obj.company_name_slug = slugify(obj.company_name)
        obj.save()

        return obj
