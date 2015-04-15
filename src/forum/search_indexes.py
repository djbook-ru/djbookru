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

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(forum__category__groups=None)

    def prepare(self, obj):
        # Fix Xapian error about terms longer then 245
        self.prepared_data = super(TopicIndex, self).prepare(obj)
        terms = self.prepared_data['text'].split(' ')
        self.prepared_data['text'] = u' '.join(term[:230] for term in terms)
        return self.prepared_data