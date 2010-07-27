from decorators import render_to
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.http import HttpResponseRedirect

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
LOGOUT_REDIRECT_URL = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')

def logout(request):
    from django.contrib.auth import logout
    from openid_consumer.views import signout as oid_signout
    
    oid_signout(request)
    logout(request)
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, LOGOUT_REDIRECT_URL)
    return HttpResponseRedirect(redirect_to)
    
