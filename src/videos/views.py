from django.views.generic.list_detail import object_list
from django.conf import settings
from .models import Video

VIDEOS_ON_PAGE = getattr(settings, 'VIDEOS_ON_PAGE', 10)


def index(request):
    qs = Video.objects.all()
    extra_context = {}
    return object_list(request, qs, VIDEOS_ON_PAGE,
                       template_name='videos/index.html',
                       extra_context=extra_context)
