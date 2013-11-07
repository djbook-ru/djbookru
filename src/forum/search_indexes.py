# encoding: utf-8

from haystack import indexes
from .models import Topic


class TopicIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    created = indexes.DateTimeField(model_attr='created')
    name = indexes.CharField(model_attr='name')
    category = indexes.CharField(model_attr='forum__category__name')
    forum = indexes.IntegerField(model_attr='forum__pk')

    def get_model(self):
        return Topic

    def get_queryset(self, using=None):
        return self.get_model().objects.filter(forum__category__groups=None)
