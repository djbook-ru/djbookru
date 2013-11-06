# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.syndication.views import Feed

from src.forum.models import Category, Post


class feed_latest_entries(Feed):

    def get_object(self, request, category_id):
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return None

    def link(self, obj):
        if obj is not None:
            return obj.get_absolute_url()
        else:
            return reverse_lazy("forum:index")

    def title(self, obj):
        if obj is not None:
            return _(u"Last messages on forum in categories {0}".format(obj.name))
        else:
            return _(u"Last messages on forum in all categories")

    def item_title(self, item):
        return unicode(item.topic.name)

    def item_author_name(self, item):
        return unicode(item.user.username)

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.updated

    def items(self, obj):
        if obj is not None:
            return Post.objects.filter(topic__forum__category=obj).order_by('-updated')[:30]
        else:
            return Post.objects.order_by('-updated')[:30]
