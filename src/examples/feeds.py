# -*- coding: utf-8 -*-

from . import models
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from src.main.templatetags.components import filter_markdown
from django.core.urlresolvers import reverse_lazy


class LatestExamplesFeed(Feed):
    title = _("Russian DjangoBook Examples")
    link = reverse_lazy('examples:index')
    description = _("Newly examples from Russian DjangoBook")

    def items(self):
        return models.Example.objects.order_by('-created')[:10]

    def item_title(self, item):
        return unicode(item)

    def item_description(self, item):
        return filter_markdown(item.content, 100)
