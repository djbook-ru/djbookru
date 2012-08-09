from accounts.backends import CustomUserBackend
from accounts.forms import UserEditForm, CreateUserForm, PasswordResetForm
from accounts.models import User, EmailConfirmation, EMAIL_CONFIRMATION_DAYS
from decorators import render_to
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset as auth_password_reset, password_reset_confirm as auth_password_reset_confirm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
LOGOUT_REDIRECT_URL = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')


@render_to('accounts/create.html')
def create(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Account created success! Confirm your email.'))
            return redirect('accounts:login')
        messages.error(request, _(u'Please correct the error below.'))
    else:
        form = CreateUserForm()
    return {
        'form': form
    }


def logout(request):
    from django.contrib.auth import logout

    logout(request)
    redirect_to = request.REQUEST.get(auth.REDIRECT_FIELD_NAME, LOGOUT_REDIRECT_URL)
    return redirect(redirect_to)


@render_to('accounts/profile.html')
def profile(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    return {
        'user_obj': user_obj
    }


@render_to('accounts/edit.html')
@login_required
def edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Profile changed success! Confirm your email if it was changed.'))
            return redirect(request.user)
        messages.error(request, _(u'Please correct the error below.'))
    else:
        form = UserEditForm(instance=request.user)
    return {
        'form': form,
    }


def confirm_email(request, confirmation_key):
    confirmation_key = confirmation_key.lower()
    user = EmailConfirmation.objects.confirm_email(confirmation_key)

    if not user:
        messages.error(request, _(u'Confirmation key expired.'))
        return redirect('/')
    else:
        messages.success(request, _(u'Email is confirmed.'))

    user.backend = "%s.%s" % (CustomUserBackend.__module__, CustomUserBackend.__name__)
    user = auth_login(request, user)

    if request.user.is_authenticated():
        return redirect('accounts:edit')

    return redirect('/')


@login_required
def resend_confirmation_email(request):
    if request.user.is_valid_email:
        messages.error(request, _(u'Your email is already confirmed.'))
    elif not request.user.email:
        messages.error(request, _(u'Add email to your profile.'))
    else:
        EmailConfirmation.objects.delete_expired_confirmations()
        if EmailConfirmation.objects.filter(user=request.user).exists():
            messages.error(request, _(u'We have sent you confirmation email. New one you can get in %(days)s days') % {
                'days': EMAIL_CONFIRMATION_DAYS
            })
        else:
            EmailConfirmation.objects.send_confirmation(request.user)
            messages.success(request, _(u'Confirmation email is sent.'))
    return redirect(request.META.get('HTTP_REFERER', '/'))


def password_reset(request):
    response = auth_password_reset(request,
        template_name='accounts/password_reset.html',
        email_template_name='accounts/email_password_reset.html',
        password_reset_form=PasswordResetForm,
        post_reset_redirect='/')

    if isinstance(response, HttpResponseRedirect):
        messages.success(request, _(u'Email with instruction how reset password is sent.'))
        return response

    return response


def password_reset_confirm(request, uidb36, token):
    return auth_password_reset_confirm(request, uidb36, token,
        post_reset_redirect=reverse('accounts:password_reset_complete'),
        template_name='accounts/password_reset_confirm.html'
    )
