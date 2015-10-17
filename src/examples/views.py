# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from .. decorators import render_to

from . import models
from . import forms


@render_to('examples/index.html')
def index(request):
    return {
        'categories': models.Category.objects.all()
    }


@render_to('examples/add.html')
@login_required
def add(request):
    form = forms.AddExampleForm(request.POST or None)

    if form.is_valid():
        form.save(request.user)
        messages.success(request, _(u'The recipe has been added successfully and will be reviewed as soon as possible.'))
        return redirect('/')

    return {
        'form': form
    }


@render_to('examples/edit.html')
@login_required
def edit(request, pk):
    example = get_object_or_404(models.Example, pk=pk)
    if example.author != request.user and not request.user.is_superuser:
        raise Http404
    form = forms.EditExampleForm(request.POST or None, instance=example)

    if form.is_valid():
        form.save(request.user)
        messages.success(request, _(u'The recipe has been edited successfully and will be reviewed as soon as possible.'))
        return redirect('/')

    return {
        'form': form
    }


@render_to('examples/category.html')
def category(request, pk):
    obj = get_object_or_404(models.Category, pk=pk)
    return {
        'category': obj
    }


@render_to('examples/detail.html')
def detail(request, pk):
    example = get_object_or_404(models.Example, pk=pk)
    if not example.approved and not request.user.is_superuser:
        raise Http404

    return {
        'obj': example
    }
