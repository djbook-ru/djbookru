from decorators import render_to
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.http import HttpResponseRedirect

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
LOGOUT_REDIRECT_URL = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')

@render_to('accounts/login.html')
def login(request):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, LOGIN_REDIRECT_URL)
    return {
        REDIRECT_FIELD_NAME: redirect_to
    }

def logout(request):
    from django.contrib.auth import logout
    from openid_consumer.views import signout as oid_signout
    
    oid_signout(request)
    logout(request)
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, LOGOUT_REDIRECT_URL)
    return HttpResponseRedirect(redirect_to)
    
