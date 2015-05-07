# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from src.accounts.tests.factories import UserFactory
from src.forum.models import Category, Forum
from src.forum.tests.factories import CategoryFactory, ForumFactory, TopicFactory


class ViewsTests(TestCase):

    def setUp(self):
        self.user = UserFactory(username='user', email='user@test.com', password='user')
        self.category = CategoryFactory()
        self.forum = ForumFactory(category=self.category)
        self.topic = TopicFactory(forum=self.forum, user=self.user)

        # some other data
        for _ in range(2):
            ForumFactory(category=self.category)
            ForumFactory()  # +1 category for each forum
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Forum.objects.count(), 5)

    def test_index(self):
        url = reverse('forum:index')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 3)
        # TODO: add tests for users online

        # test with empty DB, this is common issue to ignore new projects with empty DB
        Category.objects.all().delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 0)

    def test_users_online(self):
        pass
