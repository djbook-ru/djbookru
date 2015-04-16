# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from src.forum.models import Forum, Post


class FeedLatestPostsByForum(Feed):

    def get_object(self, request, forum_id):
        return get_object_or_404(Forum, pk=forum_id, category__groups__isnull=True)

    def link(self, obj):
        return obj.get_absolute_url()

    def title(self, obj):
        return _('Last messages on forum in categories {0}'.format(obj.name))

    def item_title(self, item):
        return item.topic.name

    def item_description(self, item):
        return item.body

    def item_author_name(self, item):
        return item.user.username

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.updated

    def items(self, obj):
        return Post.objects.filter(topic__forum=obj, topic__forum__category__groups__isnull=True) \
            .order_by('-updated')[:30]


class FeedLatestPosts(Feed):

    def link(self):
        return reverse_lazy('forum:index')

    def title(self):
        return _('Last messages on forum in all categories')

    def item_title(self, item):
        return item.topic.name

    def item_description(self, item):
        return item.body

    def item_author_name(self, item):
        return item.user.username

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.updated

    def items(self):
        return Post.objects.filter(topic__forum__category__groups__isnull=True) \
            .order_by('-updated')[:30]
