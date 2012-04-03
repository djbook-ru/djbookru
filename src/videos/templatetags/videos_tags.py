from django import template
from videos.models import Video
from random import choice

register = template.Library()


@register.inclusion_tag('videos/_last_videos.html', takes_context=True)
def last_videos(context):
    ids = Video.objects.values_list('pk', flat=True)
    context['index_video'] = Video.objects.get(pk=choice(ids))
    return context
