# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pygal
from pygal.style import LightGreenStyle

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import F, Sum, Count
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.timezone import now
from django.views.generic.list import ListView

from src.accounts.models import User
from src.decorators import render_to
from src.forum.forms import AddTopicForm, AddPostForm
from src.forum.forms import EditPostForm, MoveTopicForm
from src.forum.models import Category, Forum, Topic, Post
from src.forum.settings import POSTS_ON_PAGE
from src.utils.views import JsonResponse, object_list


@render_to('djforum/index.html')
def index(request):
    users_cached = cache.get('users_online', {})
    users_online = users_cached and User.objects.filter(
        id__in=users_cached.keys()) or []
    guests_cached = cache.get('guests_online', {})

    return {
        'categories': Category.objects.for_user(request.user),
        'users_online': users_online,
        'online_count': len(users_online),
        'guest_count': len(guests_cached),
        'users_count': User.objects.count(),
        'topics_count': Topic.objects.count(),
        'posts_count': Post.objects.count()
    }


@render_to('djforum/forum.html')
def forum(request, pk):
    forum_obj = get_object_or_404(Forum, pk=pk)

    if not forum_obj.has_access(request.user):
        raise Http404

    qs = forum_obj.topics.all()
    extra_context = {
        'forum': forum_obj
    }
    return object_list(request, qs, 20,
                       template_name='djforum/forum.html',
                       extra_context=extra_context)


def topic(request, pk):
    user = request.user
    topic = get_object_or_404(Topic, pk=pk)

    if not topic.has_access(user):
        raise Http404

    Topic.objects.filter(pk=pk).update(views=F('views') + 1)
    qs = topic.posts.all()
    form = None

    if topic.can_post(user):
        form = AddPostForm(topic, user)

    topic.mark_visited_for(user)

    extra_context = {
        'form': form,
        'forum': topic.forum,
        'topic': topic,
        'has_access': topic.has_access(user)
    }
    return object_list(request, qs, POSTS_ON_PAGE,
                       template_name='djforum/topic.html',
                       extra_context=extra_context)


class UnreadView(ListView):
    paginate_by = 20
    template_name = 'djforum/unread_topics.html'

    def get_queryset(self):
        return Topic.objects.unread(user=self.request.user)

    def get_paginator(self, *args, **kwargs):
        paginator = super(UnreadView, self).get_paginator(*args, **kwargs)
        paginator._count = Topic.objects.unread_count(
            user=self.request.user)
        return paginator

unread_topics = login_required(UnreadView.as_view())


@login_required
def mark_read_all(request):
    for forum in Forum.objects.all():
        if forum.has_access(request.user):
            forum.mark_read(request.user)
    return redirect('forum:index')


@login_required
def mark_read_forum(request, pk):
    forum = get_object_or_404(Forum, pk=pk)

    if forum.has_access(request.user):
        forum.mark_read(request.user)

    return redirect(forum)


@login_required
def my_topics(request):
    qs = Topic.objects.filter(user=request.user)
    extra_context = {}
    return object_list(request, qs, 20,
                       template_name='djforum/my_topics.html',
                       extra_context=extra_context)


@login_required
@render_to('djforum/add_topic.html')
def add_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)

    if not forum.has_access(request.user):
        raise Http404

    form = AddTopicForm(forum, request.user, request.POST or None)
    if form.is_valid():
        topic = form.save()
        return redirect(topic)
    return {
        'form': form,
        'forum': forum
    }


@login_required
@render_to('djforum/move_topic.html')
def move_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if not topic.can_edit(request.user):
        raise Http404

    form = MoveTopicForm(request.POST or None, instance=topic)

    if form.is_valid():
        form.save()
        return redirect(topic)

    return {
        'form': form,
        'topic': topic,
        'forum': topic.forum
    }


@login_required
@render_to('djforum/add_post.html')
def add_post(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if not topic.has_access(request.user):
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


@login_required
@render_to('djforum/edit_post.html')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not post.can_edit(request.user):
        messages.error(request, _('You have no permission edit this post'))
        return redirect(post.topic)

    form = EditPostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.updated = now()
        post.updated_by = request.user
        post.save()
        return redirect(post)

    return {
        'form': form,
        'topic': post.topic,
        'forum': post.topic.forum
    }


@login_required
def unsubscribe(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if topic.user == request.user:
        topic.send_response = False
        topic.save()

    return redirect(topic)


@login_required
def subscribe(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if topic.user == request.user:
        topic.send_response = True
        topic.save()

    return redirect(topic)


@login_required
def heresy_unheresy_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if topic.can_edit(request.user):
        if topic.heresy:
            topic.unmark_heresy()
        else:
            topic.mark_heresy()

    return redirect(topic)


@login_required
def close_open_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if topic.can_edit(request.user):
        if topic.closed:
            topic.open()
        else:
            topic.close()

    return redirect(topic)


@login_required
def stick_unstick_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    if topic.can_edit(request.user):
        if topic.sticky:
            topic.unstick()
        else:
            topic.stick()

    return redirect(topic)


@login_required
def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    forum = topic.forum

    if topic.can_delete(request.user) and request.method == 'POST':
        topic.delete()

    return redirect(forum)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    topic_id = post.topic_id
    forum = post.topic.forum

    if post.can_delete(request.user):
        post.delete()

    try:
        return redirect(Topic.objects.get(pk=topic_id))
    except Topic.DoesNotExist:
        return redirect(forum)


def vote(request, pk, model):
    user = request.user
    obj = get_object_or_404(model, pk=pk)

    if not user.is_authenticated():
        return JsonResponse({
            'error': ugettext('Authentication required.')
        })

    if not obj.has_access(user):
        raise Http404

    if obj.votes.filter(pk=user.pk).exists():
        obj.votes.remove(user)
        voted = False
    else:
        obj.votes.add(user)
        voted = True

    obj.update_rating()

    return JsonResponse({
        'rating': obj.rating,
        'voted': voted
    })


@render_to('djforum/statistic.html')
def statistic(request):
    most_active_users = User.objects.annotate(Count('forum_posts')) \
        .order_by('-forum_posts__count')[:10]
    most_topics_users = User.objects.annotate(Count('forum_topics')) \
        .order_by('-forum_topics__count')[:10]

    return {
        'active_users_count': User.objects.exclude(forum_posts=None).count(),
        'topics_count': Topic.objects.count(),
        'posts_count': Post.objects.count(),
        'first_post_created': Post.objects.order_by('created')[0].created,
        'views_count': Topic.objects.aggregate(Sum('views'))['views__sum'],
        'most_viewed_topics': Topic.objects.order_by('-views')[:10],
        'most_active_users': most_active_users,
        'most_topics_users': most_topics_users
    }


def posts_per_month_chart(request):
    posts_per_month = Post.objects \
        .extra(select={'year': "EXTRACT(year FROM created)",
               'month': "EXTRACT(month from created)"}) \
        .values('year', 'month').annotate(Count('id')) \
        .order_by('year', 'month')

    chart = pygal.Bar(show_legend=False, style=LightGreenStyle, x_label_rotation=45)
    chart.title = ugettext('Posts per month')
    chart.x_labels = \
        ['%s.%s' % (item['month'], item['year']) for item in posts_per_month]

    data = [{
        'value': item['id__count'],
        'label': '%s.%s' % (item['month'], item['year'])
    } for item in posts_per_month]
    chart.add(ugettext('Posts count'), data)
    content = chart.render()
    return HttpResponse(content, content_type='image/svg+xml')
