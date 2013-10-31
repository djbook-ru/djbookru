# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse

from .. decorators import render_to
from . import models


def index(request):
    qs = models.News.objects.all()
    extra_context = {}
    return object_list(request, qs, 10,
                       template_name='news/index.html',
                       extra_context=extra_context)


@render_to('news/news.html')
def news(request, pk):
    obj= get_object_or_404(models.News, pk=pk)
    if request.user.is_superuser:
        url_path = reverse('admin:news_news_changelist')
        url_path += pk
        return {
            'obj': obj,
            'url_path' : url_path
        }
    return {
        'obj': obj
    }