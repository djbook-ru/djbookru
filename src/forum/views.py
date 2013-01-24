# -*- coding: utf-8 -*-
from .. decorators import render_to
from .models import Category, Forum, Topic
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddTopicForm, AddPostForm
from django.views.generic.list_detail import object_list


@render_to('djforum/index.html')
def index(request):
    categories = [obj for obj in Category.objects.all() if obj.has_access(request.user)]

    return {
        'categories': categories
    }


@render_to('djforum/forum.html')
def forum(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    return {
        'forum': forum,
        'topics': forum.topics.all()
    }


@login_required
@render_to('djforum/add_topic.html')
def add_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    form = AddTopicForm(forum, request.user, request.POST or None)
    if form.is_valid():
        topic = form.save()
        return redirect(topic)
    return {
        'form': form,
        'forum': forum
    }


@login_required
@render_to('djforum/add_post.html')
def add_post(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if not topic.can_post(request.user):
        return redirect(topic)

    form = AddPostForm(topic, request.user, request.POST or None)
    if form.is_valid():
        post = form.save()
        return redirect(post)

    return {
        'form': form,
        'topic': topic,
        'forum': topic.forum
    }


def topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    qs = topic.posts.all()
    form = None

    if topic.can_post(request.user):
        form = AddPostForm(topic, request.user)

    extra_context = {
        'form': form,
        'forum': topic.forum,
        'topic': topic,
        'can_post': topic.can_post(request.user)
    }
    return object_list(request, qs, 100,
                       template_name='djforum/topic.html',
                       extra_context=extra_context)
