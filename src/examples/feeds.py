# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed

from . import models


class LatestExamplesFeed(Feed):
    title = _("Russian DjangoBook Examples")
    link = "/examples/"
    description = _("Newly examples from Russian DjangoBook")

    def items(self):
        return models.Example.objects.order_by('-created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
