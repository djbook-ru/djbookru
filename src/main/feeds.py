# -*- coding: utf-8 -*-

from src.examples.models import Example
from src.news.models import News
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from src.main.templatetags.components import filter_markdown
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe


class LatestFeed(Feed):
    title = _("Russian DjangoBook")
    link = reverse_lazy('examples:index')
    description = _("Newly examples from Russian DjangoBook")

    def items(self):
        examples = Example.objects.order_by('-created')[:15]
        news = News.objects.order_by('-created')[:20]

        objects = list(examples) + list(news)
        sorted(objects, key=lambda obj: obj.created)

        return objects[:15]

    def item_title(self, item):
        return unicode(item)

    def item_description(self, item):
        return filter_markdown(item.content, 100)
