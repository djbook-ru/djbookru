# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from decorators import render_to
from news.models import News
from claims.models import Claims

NEWS_ON_PAGE = getattr(settings, 'NEWS_ON_PAGE', 15)

def context_processor(request):
    return {
        'user': request.user,
        'debug': settings.DEBUG,
        'claims': Claims.statistic(),
        }

def index(request):
    qs = News.objects.all()
    extra_context = context_processor(request)
    return object_list(request, qs, NEWS_ON_PAGE,
                       template_name='news/index.html',
                       extra_context=extra_context)

@render_to('news/news.html', context_processor)
def news(request, pk):
    return {
        'object': get_object_or_404(News, pk=pk)
    }
