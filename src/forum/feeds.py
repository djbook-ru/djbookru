# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed

from src.forum.models import (Category, Post)


class FeedLatestPostsByCategory(Feed):

    def get_object(self, request, category_id):
        return get_object_or_404(Category, pk=category_id)

    def link(self, obj):
            return obj.get_absolute_url()

    def title(self, obj):
        return _(u"Last messages on forum in categories {0}".format(obj.name))

    def item_title(self, item):
        return unicode(item.topic.name)

    def item_author_name(self, item):
        return unicode(item.user.username)

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.updated

    def items(self, obj):
        return Post.objects.filter(topic__forum__category=obj).order_by('-updated')[:30]


class FeedLatestPosts(Feed):

    def link(self):
        return reverse_lazy("forum:index")

    def title(self):
        return _(u"Last messages on forum in all categories")

    def items(self):
        return Post.objects.order_by('-updated')[:30]
