from django.conf import settings
from django import get_version
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from securelayer import views as securelayer
from accounts.forms import SSAuth

def custom(request):
    context = {
        'django_version': get_version(),
        'DEBUG': settings.DEBUG,
        'site': Site.objects.get_current(),
        'debug': settings.DEBUG,
        'securelayer': True,
    }

    if reverse('accounts:login') == request.path \
       and settings.SECURELAYER_USE_WITH_DEBUG_MODE:
        protocol = request.is_secure() and 'https' or 'http'
        host = request.get_host()
        url = reverse('accounts:slogin')
        params = {
            'return_to': '%s://%s%s' % (protocol, host, url,),
            'next': request.GET.get('next', '/'),
            'form': SSAuth().as_json(caption='caption', desc='desc'),
            }
        context.update(
            {'action': 'http://%s:%s/api/show/' % (
                settings.SECURELAYER_HOST,
                settings.SECURELAYER_PORT),
             'securelayer': True,
             'redirect_form': securelayer.NextStep(initial={'data': securelayer.sign_this(params)}),
             'button_list': [{'title': _(u'Login'), 'name': 'login', 'type': 'submit'},],
             'error_desc': request.session.get('error_desc', None),
             } )
    return context
