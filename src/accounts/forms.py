# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from .. utils.forms import ReCaptchaField
from .. utils.mail import send_templated_email

from . import models


class SavePositionForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ('lng', 'lat')


class AuthenticationForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct username and password. "
                           "Note that both fields are case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class CreateUserForm(UserCreationForm):
    captcha = ReCaptchaField(label=_(u'captcha'))

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password1', 'password2', 'captcha')


class UserEditForm(forms.ModelForm):
    current_password = forms.CharField(label=_(u'Current password'), widget=forms.PasswordInput, required=False,
        help_text=_(u'Ignore if you do not have one yet.'))
    new_password = forms.CharField(label=_(u'New password'), widget=forms.PasswordInput, required=False)
    new_password_verify = forms.CharField(label=_(u'Confirm new password'), widget=forms.PasswordInput,
                                          required=False)

    class Meta:
        model = models.User
        fields = ('biography', 'email', 'signature')

    def clean(self):
        current, new, verify = map(self.cleaned_data.get,
                    ('current_password', 'new_password', 'new_password_verify'))
        if current and self.instance.has_usable_password() and not self.instance.check_password(current):
            raise forms.ValidationError(_(u'Invalid password.'))
        if new and new != verify:
            raise forms.ValidationError(_(u'The two passwords did not match.'))
        return self.cleaned_data

    def clean_email(self):
        value = self.cleaned_data['email']
        if value:
            try:
                models.User.objects.exclude(pk=self.instance.pk).get(email=value)
                raise forms.ValidationError(_(u'This email is used already.'))
            except models.User.DoesNotExist:
                pass
        return value

    def save(self, commit=True):
        password = self.cleaned_data.get('new_password')
        if password:
            self.instance.set_password(password)
        return super(UserEditForm, self).save(commit)


class PasswordResetForm(AuthPasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data["email"]
        self.users_cache = models.User.objects.filter(
                                email__iexact=email,
                                is_active=True,
                                is_valid_email=True
                            )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated active user account. Are you sure you've registered and e-mail is confirmed?"))
        return email

    def save(self, domain_override=None, email_template_name='accounts/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None, **kwargs):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = _("Password reset on %s") % site_name
            send_templated_email([user.email], subject, email_template_name, c, from_email)
