from django import get_version
from django.conf import settings
from django.contrib.sites.models import get_current_site


def custom(request):
    context = {
        'django_version': get_version(),
        'settings': settings,
        'site': get_current_site(request),
        'securelayer': False,
        'DJANGO_DOCUMENTATION_URL': settings.DJANGO_DOCUMENTATION_URL,
        'DJANGO_DOCUMENTATION_SITEMAP_URL': settings.DJANGO_DOCUMENTATION_SITEMAP_URL
    }
    return context
