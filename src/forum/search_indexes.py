# encoding: utf-8

from haystack.indexes import *
from haystack import site

from . import models


class TopicIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    created = DateTimeField(model_attr='created')
    name = CharField(model_attr='name')
    category = CharField(model_attr='forum__category__name')
    forum = IntegerField(model_attr='forum__pk')

site.register(models.Topic, TopicIndex)
