# -*- coding: utf-8 -*-

from . import models
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from src.main.templatetags.components import filter_markdown
from django.core.urlresolvers import reverse_lazy


class LatestNewsFeed(Feed):
    title = _("Russian DjangoBook")
    link = reverse_lazy('news:index')
    description = _("The freshest news about Russian version of DjangoBook")

    def items(self):
        return models.News.objects.approved().order_by('-created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return filter_markdown(item.content)
