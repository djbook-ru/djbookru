from django.conf import settings 
from django import get_version
from django.contrib.sites.models import Site

def custom(request):
    return {
        'django_version': get_version(),
        'DEBUG': settings.DEBUG,
        'site': Site.objects.get_current()
    }