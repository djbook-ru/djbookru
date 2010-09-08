from django import forms
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from utils.forms import AjaxForm
from django.utils.translation import gettext_lazy as _

class FeedbackForm(forms.Form, AjaxForm):
    email = forms.EmailField(label=_(u'email'), required=False)
    message = forms.CharField(label=_(u'message'), widget=forms.Textarea())
    
    def send(self, request):
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        user_agent_data = 'User agent: %s' % request.META.get('HTTP_USER_AGENT')
        timestamp = 'Time: %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = '%s\n\n%s\n%s\n%s\n%s' % (message, user_agent_data, timestamp)
        headers = {'Reply-To': email} if email else None
        
        EmailMessage(settings.FEEDBACK_SUBJECT, message, email, \
                     [settings.FEEDBACK_EMAIL], headers=headers).send()