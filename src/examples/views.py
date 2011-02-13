# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect
from decorators import render_to
from examples.models import Category, Example
from examples.forms import AddExampleForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

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
        messages.success(request, _(u'Example was added success and will be reviewed as soon as possible.'))
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
    return {
        'obj': get_object_or_404(Example.objects.approved(), pk=pk)
    }
