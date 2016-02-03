# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from haystack.forms import SearchForm as HaystackSearchForm
from haystack_static_pages.models import StaticPage

from .. forum.models import Topic
from .. examples.models import Example
from .. news.models import News
from .. utils.forms import ReCaptchaField


class FeedbackForm(forms.Form):
    email = forms.EmailField(label=_(u'Email'), required=False)
    message = forms.CharField(label=_(u'Message'), widget=forms.Textarea())
    referer = forms.CharField(required=False, widget=forms.HiddenInput())
    captcha = ReCaptchaField(label=_(u'Captcha'))

    def send(self, request):
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        user_agent_data = 'User agent: %s' % request.META.get('HTTP_USER_AGENT')
        timestamp = 'Time: %s' % timezone.now().strftime('%H:%M:%S %m-%d-%Y')
        referer = 'Referer: %s' % self.cleaned_data['referer']
        message = '%s\n\n%s\n%s\n%s' % (message, user_agent_data, timestamp, referer)
        headers = {'Reply-To': email} if email else None

        EmailMessage(settings.FEEDBACK_SUBJECT, message, email, \
                     [a[1] for a in settings.ADMINS], headers=headers).send()


def content_choices():
    choices = (
        ('', _(u'All')),
    )
    try:
        choices += (
            (ContentType.objects.get_for_model(Example).pk, _(u'Recipes')),
            (ContentType.objects.get_for_model(Topic).pk, _(u'Forum')),
            (ContentType.objects.get_for_model(News).pk, _(u'News')),
            (ContentType.objects.get_for_model(StaticPage).pk, _(u'Documentation')),
        )
    except RuntimeError:
        pass
    return choices


class SearchForm(HaystackSearchForm):
    content = forms.ChoiceField(choices=content_choices(), label=_(u'Search by'), required=False)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data['q']:
            return self.no_query_found()

        content_type_id = self.cleaned_data.get('content', '')
        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if content_type_id:
            sqs = sqs.models(ContentType.objects.get(pk=content_type_id).model_class())

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
