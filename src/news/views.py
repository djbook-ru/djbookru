# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.views.decorators.csrf import csrf_exempt

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
    return {
        'obj': get_object_or_404(models.News, pk=pk)
    }
    
    
@csrf_exempt
@render_to('news/edit.html')
def edit(request, pk):
    obj = get_object_or_404(models.News, pk=pk)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = models.NewsForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return news(request, obj.id)
        else:
            form = models.NewsForm(instance=obj)
            return {
                'obj': obj,
                'form': form
            }
    else:
       return news(request, obj.id) 