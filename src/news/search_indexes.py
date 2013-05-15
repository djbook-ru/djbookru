# -*- coding: utf-8 -*-

from haystack.indexes import *
from haystack import site
from django.utils.translation import ugettext_lazy as _
from . import models


class NewsIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')
    created = DateTimeField(model_attr='created')

site.register(models.News, NewsIndex)
