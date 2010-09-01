from decorators import render_to
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.http import HttpResponseRedirect
from accounts.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserEditForm

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
LOGOUT_REDIRECT_URL = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')

def logout(request):
    from django.contrib.auth import logout
    from openid_consumer.views import signout as oid_signout
    
    oid_signout(request)
    logout(request)
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, LOGOUT_REDIRECT_URL)
    return HttpResponseRedirect(redirect_to)

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
            return redirect(request.user)
    else:
        form = UserEditForm( instance=request.user)
    return {
        'form': form
    }
    
