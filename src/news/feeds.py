# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed

from . import models


class LatestNewsFeed(Feed):
    title = _("Russian DjangoBook")
    link = "/news/"
    description = _("The freshest news about Russian version of DjangoBook")

    def items(self):
        return models.News.objects.order_by('-created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
