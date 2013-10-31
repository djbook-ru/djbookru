# encoding: utf-8

from haystack.indexes import *
from haystack import site

from .models import Topic


class TopicIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    created = DateTimeField(model_attr='created')
    name = CharField(model_attr='name')
    category = CharField(model_attr='forum__category__name')
    forum = IntegerField(model_attr='forum__pk')

    def index_queryset(self):
        return Topic.objects.filter(forum__category__groups=None)

site.register(Topic, TopicIndex)
