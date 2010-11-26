from django.conf import settings 
from django import get_version

def custom(request):
    return {
        'django_version': get_version(),
        'DEBUG': settings.DEBUG
    }