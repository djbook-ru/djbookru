# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404

from decorators import render_to
from examples.models import Category, Example
from claims.models import Claims

def context_processor(request):
    return {
        'user': request.user,
        'debug': settings.DEBUG,
        'claims': Claims.statistic(),
        }

@render_to('examples/index.html', context_processor)
def index(request):
    return {
        'categories': Category.objects.all()
    }

@render_to('examples/category.html', context_processor)
def category(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    return {
        'category': obj
    }

@render_to('examples/detail.html', context_processor)
def detail(request, pk):
    return {
        'obj': get_object_or_404(Example.objects.approved(), pk=pk)
    }
