from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from dinette.models import Ftopics ,Reply

#create a form from this Ftopics and use this when posting the a Topic
class FtopicForm(ModelForm):
    subject = forms.CharField(label=_(u'subject'), widget = forms.TextInput(attrs={"size":90}))
    message = forms.CharField(label=_(u'message'), widget = forms.Textarea(attrs={"cols":90, "rows":10}))
    
    class Meta:
        model = Ftopics
        fields = ('subject', 'message',)

#create a form from Reply
class ReplyForm(ModelForm):
    message = forms.CharField(label=_(u'message'), widget = forms.Textarea(attrs={"cols":90, "rows":10}))
    class Meta:
        model = Reply
        fields = ('message',)
            