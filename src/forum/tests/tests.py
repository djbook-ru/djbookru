# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from time import sleep

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase

from src.accounts.tests.factories import UserFactory, GroupFactory
from src.forum.models import Category, Forum, Topic
from src.forum.tests.factories import CategoryFactory, ForumFactory, TopicFactory, PostFactory


class BaseTestCase(TestCase):

    def setUp(self):
        self.anonymous_user = AnonymousUser()
        self.some_user = UserFactory(username='user', email='user@test.com', password='user')
        self.group_user = UserFactory(username='user1', email='user1@test.com', password='user1')
        self.group = GroupFactory()
        self.group_user.groups.add(self.group)

    def login(self, user):
        # it is not a magic, just password is equal to username
        self.assertTrue(self.client.login(username=user.email, password=user.username))


class ViewsTests(BaseTestCase):

    def test_index(self):
        url = reverse('forum:index')

        public_category = CategoryFactory()
        private_category = CategoryFactory()
        private_category.groups.add(self.group)

        # test anonymous
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['categories']), [public_category])

        # test some user
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['categories']), [public_category])

        # test group user
        self.login(self.group_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['categories']), [public_category, private_category])

        # add more data
        for _ in range(2):
            ForumFactory(category=public_category)
            ForumFactory(category=private_category)
            ForumFactory()  # +1 category for each forum

        self.assertEqual(Category.objects.count(), 4)

        # test anonymous
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 3)

        # test some user
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 3)

        # test group user
        self.login(self.group_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 4)

        # TODO: add tests for users online

        # test with empty DB, this is common issue to ignore new projects with empty DB
        self.client.logout()
        Category.objects.all().delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 0)

    def test_forum(self):
        forum = ForumFactory()

        url = reverse('forum:forum', args=(forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:forum', args=(123,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ModelTests(BaseTestCase):

    def test_category(self):
        public_category = CategoryFactory()
        private_category = CategoryFactory()
        private_category.groups.add(self.group)

        self.assertTrue(public_category.get_absolute_url())

        self.assertTrue(public_category.has_access(self.anonymous_user))
        self.assertTrue(public_category.has_access(self.some_user))
        self.assertTrue(public_category.has_access(self.group_user))

        self.assertFalse(private_category.has_access(self.anonymous_user))
        self.assertFalse(private_category.has_access(self.some_user))
        self.assertTrue(private_category.has_access(self.group_user))

        self.assertEqual(list(Category.objects.for_user(self.anonymous_user)), [public_category])
        self.assertEqual(list(Category.objects.for_user(self.some_user)), [public_category])
        self.assertEqual(list(Category.objects.for_user(self.group_user)),
                         [public_category, private_category])

    def test_forum(self):
        public_forum = ForumFactory()
        private_forum = ForumFactory()
        private_forum.category.groups.add(self.group)

        self.assertTrue(public_forum.get_absolute_url())

        self.assertTrue(public_forum.has_access(self.anonymous_user))
        self.assertTrue(public_forum.has_access(self.some_user))
        self.assertTrue(public_forum.has_access(self.group_user))

        self.assertFalse(private_forum.has_access(self.anonymous_user))
        self.assertFalse(private_forum.has_access(self.some_user))
        self.assertTrue(private_forum.has_access(self.group_user))

    def test_topic(self):
        public_topic = TopicFactory()
        private_topic = TopicFactory()
        private_topic.forum.category.groups.add(self.group)

        self.assertTrue(public_topic.get_absolute_url())

        self.assertTrue(public_topic.has_access(self.anonymous_user))
        self.assertTrue(public_topic.has_access(self.some_user))
        self.assertTrue(public_topic.has_access(self.group_user))

        self.assertFalse(private_topic.has_access(self.anonymous_user))
        self.assertFalse(private_topic.has_access(self.some_user))
        self.assertTrue(private_topic.has_access(self.group_user))

    def test_post(self):
        public_post = PostFactory()
        private_post = PostFactory()
        private_post.topic.forum.category.groups.add(self.group)

        self.assertTrue(public_post.get_absolute_url())

        self.assertTrue(public_post.has_access(self.anonymous_user))
        self.assertTrue(public_post.has_access(self.some_user))
        self.assertTrue(public_post.has_access(self.group_user))

        self.assertFalse(private_post.has_access(self.anonymous_user))
        self.assertFalse(private_post.has_access(self.some_user))
        self.assertTrue(private_post.has_access(self.group_user))

    def test_read_unread(self):
        # we do not track this for anonymous user, so just test API
        topic = TopicFactory()
        for _ in range(3):
            PostFactory(topic=topic)

        self.assertFalse(topic.has_unread(self.anonymous_user))
        self.assertTrue(topic.has_unread(self.some_user))
        self.assertTrue(topic.has_unread(self.group_user))

        self.assertFalse(topic.forum.has_unread(self.anonymous_user))
        self.assertTrue(topic.forum.has_unread(self.some_user))
        self.assertTrue(topic.forum.has_unread(self.group_user))

        # mark topic as read
        topic.mark_visited_for(self.anonymous_user)
        topic.mark_visited_for(self.some_user)

        topic.refresh_from_db()
        self.assertFalse(topic.has_unread(self.some_user))
        self.assertFalse(topic.forum.has_unread(self.some_user))
        self.assertTrue(topic.has_unread(self.group_user))
        self.assertTrue(topic.forum.has_unread(self.group_user))

        # add one more post
        # FIXME: sleep is a crap, but MySQL does not save milliseconds, so visit time and
        # new post time are equal
        sleep(1)
        PostFactory(topic=topic)
        topic.refresh_from_db()
        self.assertTrue(topic.has_unread(self.some_user))
        self.assertTrue(topic.forum.has_unread(self.some_user))
        self.assertTrue(topic.has_unread(self.group_user))
        self.assertTrue(topic.forum.has_unread(self.group_user))

        # test Forum.mark_read
        topic.forum.mark_read(self.some_user)
        topic.refresh_from_db()
        self.assertFalse(topic.has_unread(self.some_user))
        self.assertFalse(topic.forum.has_unread(self.some_user))
        self.assertTrue(topic.has_unread(self.group_user))
        self.assertTrue(topic.forum.has_unread(self.group_user))

        topic1 = TopicFactory(forum=topic.forum)
        self.assertTrue(topic1.has_unread(self.some_user))
        self.assertTrue(topic.forum.has_unread(self.some_user))
        self.assertFalse(topic.has_unread(self.some_user))
        self.assertTrue(topic1.has_unread(self.group_user))
        self.assertTrue(topic.has_unread(self.group_user))
        self.assertTrue(topic.forum.has_unread(self.group_user))

        topic.forum.mark_read(self.some_user)
        topic.refresh_from_db()
        self.assertFalse(topic1.has_unread(self.some_user))
        self.assertFalse(topic.forum.has_unread(self.some_user))
        self.assertFalse(topic.has_unread(self.some_user))
        self.assertTrue(topic1.has_unread(self.group_user))
        self.assertTrue(topic.has_unread(self.group_user))
        self.assertTrue(topic.forum.has_unread(self.group_user))

    def test_topic_manager(self):
        public_forum = ForumFactory()
        private_forum = ForumFactory()
        private_forum.category.groups.add(self.group)

        pubic_topic = TopicFactory(forum=public_forum)
        private_topic = TopicFactory(forum=private_forum)

        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.some_user, public_forum)),
            [pubic_topic])
        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.some_user, private_forum)),
            [])
        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.group_user, public_forum)),
            [pubic_topic])
        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.group_user, private_forum)),
            [private_topic])

        self.assertEqual(
            list(Topic.objects.unread(self.some_user)),
            [pubic_topic])
        self.assertEqual(
            list(Topic.objects.unread(self.group_user)),
            [pubic_topic, private_topic])

        self.assertEqual(Topic.objects.unread_count(self.some_user), 1)
        self.assertEqual(Topic.objects.unread_count(self.group_user), 2)
