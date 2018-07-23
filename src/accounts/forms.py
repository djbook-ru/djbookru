# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from src.accounts.models import User


class SavePositionForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('lng', 'lat')


class AuthenticationForm(forms.Form):
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields are case-sensitive."),
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
                    self.error_messages['invalid_login'],
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.
        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserEditForm(forms.ModelForm):
    current_password = forms.CharField(
        label=_('Current password'), widget=forms.PasswordInput, required=False,
        help_text=_('Ignore if you do not have one yet. We recommend setup password, '
                    'so you can use it to login, because sometime we broke login via '
                    'some external service.'))
    new_password = forms.CharField(
        label=_('New password'), widget=forms.PasswordInput, required=False)
    new_password_verify = forms.CharField(
        label=_('Confirm new password'), widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'biography', 'email', 'country', 'location', 'signature')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = _('We use this an small pieces of info.')

    def clean(self):
        current, new, verify = map(
            self.cleaned_data.get,
            ('current_password', 'new_password', 'new_password_verify'))
        if current and self.instance.has_usable_password() \
                and not self.instance.check_password(current):
            raise forms.ValidationError(_('Invalid password.'))
        if new and new != verify:
            raise forms.ValidationError(_('The two passwords did not match.'))
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.exclude(pk=self.instance.pk).filter(username__iexact=username):
            raise forms.ValidationError(_('A user with that username already exists.'))
        return username

    def clean_email(self):
        value = self.cleaned_data['email']
        if value:
            try:
                User.objects.exclude(pk=self.instance.pk).get(email=value)
                raise forms.ValidationError(_('This email is used already.'))
            except User.DoesNotExist:
                pass
        return value

    def save(self, commit=True):
        password = self.cleaned_data.get('new_password')
        if password:
            self.instance.set_password(password)
        return super(UserEditForm, self).save(commit)
