# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from decorators import render_to

from examples.models import Category, Example
from examples.forms import AddExampleForm
from djangobb_forum.models import Topic

@render_to('examples/index.html')
def index(request):
    return {
        'categories': Category.objects.all()
    }

@render_to('examples/add.html')
@login_required
def add(request):
    form = AddExampleForm(request.POST or None)

    if form.is_valid():
        form.save(request.user)
        messages.success(request, _(u'The recipe has been added successfully and will be reviewed as soon as possible.'))
        return redirect('/')

    return {
        'form': form
    }

@render_to('examples/category.html',)
def category(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    return {
        'category': obj
    }

@render_to('examples/detail.html')
def detail(request, pk):
    try:
        example = Example.objects.get(pk=pk)
        if not example.approved and not request.user.is_superuser:
            raise Http404
    except Example.DoesNotExist:
        raise Http404

    try:
        topic = Topic.objects.get(pk=example.topic_id)
    except Topic.DoesNotExist:
        topic = None

    return {
        'obj': example,
        'topic': topic
    }
