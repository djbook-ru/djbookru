# encoding: utf-8

from haystack.indexes import *
from haystack import site

import news.models as models


class NewsIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')
    created = DateTimeField(model_attr='created')
    author = CharField(model_attr='author')

site.register(models.News, NewsIndex)
