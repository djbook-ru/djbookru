from django.contrib import auth
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _

from decorators import render_to
from securelayer import views as securelayer

from accounts.models import User
from accounts.forms import UserEditForm, CreateUserForm, SSAuth

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
LOGOUT_REDIRECT_URL = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')

@render_to('accounts/create.html')
def create(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Account created success!'))
            return redirect('accounts:login')
        messages.error(request, _(u'Please correct the error below.'))
    else:
        form = CreateUserForm()
    return {
        'form': form
    }

def logout(request):
    from django.contrib.auth import logout
    from openid_consumer.views import signout as oid_signout

    oid_signout(request)
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
            messages.success(request, _(u'Profile changed success!'))
            return redirect(request.user)
        messages.error(request, _(u'Please correct the error below.'))
    else:
        form = UserEditForm(instance=request.user)
    return {
        'form': form
    }

def slogin(request):
    if request.method == 'GET':
        session_key = request.GET.get('ss', None)
        next_url = request.GET.get('next', '/')
        if session_key:
            ready, response, cookie = securelayer.secured_request(
                '/api/data/', {'service': 'data'}, session_key)
            form = SSAuth()
            form.import_json(response.get('data', None))
            if 'JSON' == getattr(form, 'source', None):
                if form.is_valid():
                    username = form.cleaned_data.get('username', None)
                    password = form.cleaned_data.get('password', None)
                    user = auth.authenticate(username=username, password=password)
                    if user and user.is_active:
                        auth.login(request, user)
                        ready, response, cookie = securelayer.secured_request(
                            '/api/close/', {'service': 'close'}, session_key)
                        return redirect(next_url)
                    else:
                        request.session['error_desc'] = _(u'Wrong user\'s credentials.')
                        return redirect(reverse('accounts:login'))
    return redirect('/')
