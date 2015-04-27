# -*- coding: utf-8 -*-

from haystack import indexes
from .models import Example


class ExampleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    created = indexes.DateTimeField(model_attr='created')
    author = indexes.CharField(model_attr='author')

    def get_model(self):
        return Example

    def prepare(self, obj):
        # Fix Xapian error about terms longer then 245
        self.prepared_data = super(ExampleIndex, self).prepare(obj)
        terms = self.prepared_data['text'].split(' ')
        self.prepared_data['text'] = u' '.join(term[:230] for term in terms)
        return self.prepared_data
