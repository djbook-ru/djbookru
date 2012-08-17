# -*- coding: utf-8 -*-

from haystack.indexes import *
from haystack import site

from . import models


class ExampleIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')
    created = DateTimeField(model_attr='created')
    author = CharField(model_attr='author')

site.register(models.Example, ExampleIndex)
