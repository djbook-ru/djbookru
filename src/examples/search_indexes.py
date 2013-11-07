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
