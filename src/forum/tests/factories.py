# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import factory

from src.accounts.tests.factories import UserFactory
from src.forum.models import Category, Forum, Topic, Post


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda i: 'Category #%s' % i)

    class Meta:
        model = Category


class ForumFactory(factory.django.DjangoModelFactory):
    category = factory.SubFactory(CategoryFactory)
    name = factory.Sequence(lambda i: 'Forum #%s' % i)

    class Meta:
        model = Forum


class TopicFactory(factory.django.DjangoModelFactory):
    forum = factory.SubFactory(ForumFactory)
    name = factory.Sequence(lambda i: 'Topic #%s' % i)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Topic

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        if create:
            PostFactory(topic=obj, user=obj.user)
        factory.DjangoModelFactory._after_postgeneration(obj, create, results)


class PostFactory(factory.django.DjangoModelFactory):
    topic = factory.SubFactory(TopicFactory)
    user = factory.SubFactory(UserFactory)
    body = factory.Sequence(lambda i: 'Some post #%s' % i)

    class Meta:
        model = Post
