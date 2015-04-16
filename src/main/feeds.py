# -*- coding: utf-8 -*-

from src.examples.models import Example
from src.news.models import News
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from src.main.templatetags.components import filter_markdown
from django.core.urlresolvers import reverse_lazy
from operator import attrgetter


class LatestFeed(Feed):
    title = _("Russian DjangoBook")
    link = reverse_lazy('examples:index')
    description = _("Newly examples from Russian DjangoBook")

    def items(self):
        examples = Example.objects.approved().order_by('-created')[:15]
        news = News.objects.approved().order_by('-created')[:20]

        objects = list(examples) + list(news)

        objects.sort(key=attrgetter('created'), reverse=True)

        return objects[:15]

    def item_title(self, item):
        return unicode(item)

    def item_description(self, item):
        return filter_markdown(item.content, 100)
