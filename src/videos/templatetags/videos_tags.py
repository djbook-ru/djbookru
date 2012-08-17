# -*- coding: utf-8 -*-

from random import choice

from django import template

from .. import models

register = template.Library()


@register.inclusion_tag('videos/_last_videos.html', takes_context=True)
def last_videos(context):
    ids = models.Video.objects.values_list('pk', flat=True)
    if ids:
        context['index_video'] = models.Video.objects.get(pk=choice(ids))
    return context
