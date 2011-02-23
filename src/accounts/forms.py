from django import forms
from accounts.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from utils.forms import ReCaptchaField
from securelayer import SecuredForm

class CreateUserForm(UserCreationForm):
    captcha = ReCaptchaField(label=_(u'captcha'))

class SSAuth(SecuredForm):
    username = forms.CharField(label=ugettext("Username"), max_length=30)
    password = forms.CharField(label=ugettext("Password"), widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    current_password = forms.CharField(label=_(u'Current password'), widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(label=_(u'New password'), widget=forms.PasswordInput, required=False)
    new_password_verify = forms.CharField(label=_(u'Confirm new password'), widget=forms.PasswordInput,
                                          required=False)
    class Meta:
        model = User
        fields = ('biography', 'email')

    def clean(self):
        current, new, verify = map(self.cleaned_data.get,
                    ('current_password', 'new_password', 'new_password_verify'))
        if current and not self.instance.check_password(current):
            raise forms.ValidationError(_(u'Invalid password.'))
        if new and new != verify:
            raise forms.ValidationError(_(u'The two passwords did not match.'))
        return self.cleaned_data

    def clean_email(self):
        value = self.cleaned_data['email']
        if value:
            try:
                User.objects.exclude(pk=self.instance.pk).get(email=value)
                raise forms.ValidationError(_(u'This email is used already.'))
            except User.DoesNotExist:
                pass
        return value

    def save(self, commit=True):
        password = self.cleaned_data.get('new_password')
        if password:
            self.instance.set_password(password)
        return super(UserEditForm, self).save(commit)
