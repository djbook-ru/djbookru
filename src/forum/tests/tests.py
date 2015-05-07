# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase

from src.accounts.tests.factories import UserFactory, GroupFactory
from src.forum.models import Category, Forum
from src.forum.tests.factories import CategoryFactory, ForumFactory, TopicFactory, PostFactory


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

    def test_forum(self):
        url = reverse('forum:forum', args=(self.forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:forum', args=(123,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ModelTests(TestCase):

    def setUp(self):
        self.anonymous_user = AnonymousUser()
        self.some_user = UserFactory()
        self.group_user = UserFactory()
        self.group = GroupFactory()
        self.group_user.groups.add(self.group)

    def test_category(self):
        public_category = CategoryFactory()
        privat_category = CategoryFactory()
        privat_category.groups.add(self.group)

        self.assertTrue(public_category.has_access(self.anonymous_user))
        self.assertTrue(public_category.has_access(self.some_user))
        self.assertTrue(public_category.has_access(self.group_user))

        self.assertFalse(privat_category.has_access(self.anonymous_user))
        self.assertFalse(privat_category.has_access(self.some_user))
        self.assertTrue(privat_category.has_access(self.group_user))

    def test_forum(self):
        public_forum = ForumFactory()
        privat_forum = ForumFactory()
        privat_forum.category.groups.add(self.group)

        self.assertTrue(public_forum.has_access(self.anonymous_user))
        self.assertTrue(public_forum.has_access(self.some_user))
        self.assertTrue(public_forum.has_access(self.group_user))

        self.assertFalse(privat_forum.has_access(self.anonymous_user))
        self.assertFalse(privat_forum.has_access(self.some_user))
        self.assertTrue(privat_forum.has_access(self.group_user))

    def test_topic(self):
        public_topic = TopicFactory()
        privat_topic = TopicFactory()
        privat_topic.forum.category.groups.add(self.group)

        self.assertTrue(public_topic.has_access(self.anonymous_user))
        self.assertTrue(public_topic.has_access(self.some_user))
        self.assertTrue(public_topic.has_access(self.group_user))

        self.assertFalse(privat_topic.has_access(self.anonymous_user))
        self.assertFalse(privat_topic.has_access(self.some_user))
        self.assertTrue(privat_topic.has_access(self.group_user))

    def test_post(self):
        public_post = PostFactory()
        privat_post = PostFactory()
        privat_post.topic.forum.category.groups.add(self.group)

        self.assertTrue(public_post.has_access(self.anonymous_user))
        self.assertTrue(public_post.has_access(self.some_user))
        self.assertTrue(public_post.has_access(self.group_user))

        self.assertFalse(privat_post.has_access(self.anonymous_user))
        self.assertFalse(privat_post.has_access(self.some_user))
        self.assertTrue(privat_post.has_access(self.group_user))
