# -*- coding: utf-8 -*-
from .. decorators import render_to
from .forms import AddTopicForm, AddPostForm
from .models import Category, Forum, Topic, Post
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_list
from django.core.cache import cache
from src.accounts.models import User


@render_to('djforum/index.html')
def index(request):
    users_cached = cache.get('users_online', {})
    users_online = users_cached and User.objects.filter(id__in=users_cached.keys()) or []
    guests_cached = cache.get('guests_online', {})
    guest_count = len(guests_cached)
    users_count = len(users_online)

    categories = [obj for obj in Category.objects.all() if obj.has_access(request.user)]

    return {
        'categories': categories,
        'users_online': users_online,
        'online_count': users_count,
        'guest_count': guest_count,
        'users_count': User.objects.count(),
        'topics_count': Topic.objects.count(),
        'posts_count': Post.objects.count()
    }


@render_to('djforum/forum.html')
def forum(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    qs = forum.topics.all()
    extra_context = {
        'forum': forum
    }
    return object_list(request, qs, 20,
                       template_name='djforum/forum.html',
                       extra_context=extra_context)


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
    Topic.objects.filter(pk=pk).update(views=F('views') + 1)
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
