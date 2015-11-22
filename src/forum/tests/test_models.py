# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

from time import sleep
from datetime import timedelta

from django.utils import timezone

from src.forum.models import Category, Topic
from src.forum.tests.factories import CategoryFactory, ForumFactory, TopicFactory, PostFactory
from src.forum.settings import FORUM_EDIT_TIMEOUT
from .base import BaseTestCase


class CategoryTest(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super(CategoryTest, cls).setUpTestData()

        cls.public_category = CategoryFactory()
        cls.private_category = CategoryFactory()
        cls.private_category.groups.add(cls.group)

    def test_get_absolute_url(self):

        self.assertTrue(self.public_category.get_absolute_url())

    def test_anonymous_user_has_access_to_public_category(self):
        self.assertTrue(self.public_category.has_access(self.anonymous_user))

    def test_authenticated_user_has_access_to_public_category(self):
        self.assertTrue(self.public_category.has_access(self.some_user))

    def test_group_user_has_access_to_public_category(self):
        self.assertTrue(self.public_category.has_access(self.group_user))

    def test_superuser_user_has_access_to_public_category(self):
        self.assertTrue(self.public_category.has_access(self.superuser))

    def test_anonymous_user_has_no_access_to_private_category(self):
        self.assertFalse(self.private_category.has_access(self.anonymous_user))

    def test_authenticated_user_has_no_access_to_private_category(self):
        self.assertFalse(self.private_category.has_access(self.some_user))

    def test_group_user_has_access_to_private_category(self):
        self.assertTrue(self.private_category.has_access(self.group_user))

    def test_superuser_user_has_access_to_private_category(self):
        self.assertTrue(self.private_category.has_access(self.superuser))

    def test_anonymous_user_accessable_categories(self):
        self.assertSequenceEqual(list(Category.objects.for_user(self.anonymous_user)), [self.public_category])

    def test_authenticated_user_accessable_categories(self):
        self.assertSequenceEqual(list(Category.objects.for_user(self.some_user)), [self.public_category])

    def test_group_user_accessable_categories(self):
        self.assertSequenceEqual(list(Category.objects.for_user(self.group_user)), [self.public_category, self.private_category])

    def test_superuser_accessable_categories(self):
        self.assertSequenceEqual(list(Category.objects.for_user(self.superuser)), [self.public_category, self.private_category])


class ForumTest(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super(ForumTest, cls).setUpTestData()

        cls.public_forum = ForumFactory()
        cls.private_forum = ForumFactory()
        cls.private_forum.category.groups.add(cls.group)

        cls.forum = ForumFactory()
        cls.topic = TopicFactory(forum=cls.forum)

    def setUp(self):
        self.topic.refresh_from_db()

    def test_has_unread_for_anonymous_user(self):
        self.assertFalse(self.forum.has_unread(self.anonymous_user))

    def test_has_unread_for_authenticated_user(self):
        self.assertTrue(self.forum.has_unread(self.some_user))

    def test_has_unread_for_group_user(self):
        self.assertTrue(self.forum.has_unread(self.group_user))

    def test_has_unread_if_topic_is_visited(self):

        # XXX wtf?
        self.topic.mark_visited_for(self.anonymous_user)
        self.topic.mark_visited_for(self.some_user)

        # XXX wtf?
        self.assertFalse(self.forum.has_unread(self.some_user))
        self.assertTrue(self.forum.has_unread(self.group_user))

    def test_has_unread_for_authenticated_user_if_new_post_was_created(self):

        # add one more post
        # FIXME: sleep is a crap, but MySQL does not save milliseconds, so visit time and
        # new post time are equal
        sleep(1)
        PostFactory(topic=self.topic)
        self.topic.refresh_from_db()
        self.assertTrue(self.forum.has_unread(self.some_user))

    def test_has_unread_for_group_user_if_new_post_was_created(self):

        # add one more post
        # FIXME: sleep is a crap, but MySQL does not save milliseconds, so visit time and
        # new post time are equal
        sleep(1)
        PostFactory(topic=self.topic)
        self.topic.refresh_from_db()
        self.assertTrue(self.forum.has_unread(self.group_user))

    def test_has_unread_mark_read(self):

        self.forum.mark_read(self.some_user)
        self.assertFalse(self.forum.has_unread(self.some_user))
        self.assertTrue(self.forum.has_unread(self.group_user))

    def test_has_unread_if_new_topic_created(self):

        topic1 = TopicFactory(forum=self.forum)
        self.assertTrue(self.forum.has_unread(self.some_user))
        self.assertTrue(self.forum.has_unread(self.group_user))

    def test_get_absolute_url(self):
        self.assertTrue(self.public_forum.get_absolute_url())

    def test_anonymous_user_has_access_to_public_forum(self):
        self.assertTrue(self.public_forum.has_access(self.anonymous_user))

    def test_authenticated_user_user_has_access_to_public_forum(self):
        self.assertTrue(self.public_forum.has_access(self.some_user))

    def test_group_user_user_has_access_to_public_forum(self):
        self.assertTrue(self.public_forum.has_access(self.group_user))

    def test_superuser_user_has_access_to_public_forum(self):
        self.assertTrue(self.public_forum.has_access(self.superuser))

    def test_anonymous_user_has_no_accesse_to_private_forum(self):
        self.assertFalse(self.private_forum.has_access(self.anonymous_user))

    def test_authenticated_user_user_has_no_accesse_to_private_forum(self):
        self.assertFalse(self.private_forum.has_access(self.some_user))

    def test_group_user_user_has_accesse_to_private_forum(self):
        self.assertTrue(self.private_forum.has_access(self.group_user))

    def test_superuser_user_has_accesse_to_private_forum(self):
        self.assertTrue(self.private_forum.has_access(self.superuser))


class PostTest(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super(PostTest, cls).setUpTestData()

        cls.public_post = PostFactory()
        cls.private_post = PostFactory()
        cls.private_post.topic.forum.category.groups.add(cls.group)

    def setUp(self):
        self.public_post.refresh_from_db()

    def test_get_absolute_url(self):
        self.assertTrue(self.public_post.get_absolute_url())

    def test_post_is_expired(self):
        self.assertFalse(self.public_post.expired)

    def test_anonymous_user_has_access_to_public_post(self):
        self.assertTrue(self.public_post.has_access(self.anonymous_user))

    def test_authenticated_user_user_has_access_to_public_post(self):
        self.assertTrue(self.public_post.has_access(self.some_user))

    def test_group_user_user_has_access_to_public_post(self):
        self.assertTrue(self.public_post.has_access(self.group_user))

    def test_superuser_user_has_access_to_public_post(self):
        self.assertTrue(self.public_post.has_access(self.superuser))

    def test_anonymous_user_has_no_accesse_to_private_post(self):
        self.assertFalse(self.private_post.has_access(self.anonymous_user))

    def test_authenticated_user_user_has_no_accesse_to_private_post(self):
        self.assertFalse(self.private_post.has_access(self.some_user))

    def test_group_user_user_has_accesse_to_private_post(self):
        self.assertTrue(self.private_post.has_access(self.group_user))

    def test_superuser_user_has_accesse_to_private_post(self):
        self.assertTrue(self.private_post.has_access(self.superuser))

    def test_anonymous_user_cannot_delete_public_post(self):
        self.assertFalse(self.public_post.can_delete(self.anonymous_user))

    def test_authenticated_user_cannot_delete_public_post(self):
        self.assertFalse(self.public_post.can_delete(self.some_user))

    def test_group_user_cannot_delete_private_post(self): # XXX private
        self.assertFalse(self.private_post.can_delete(self.group_user))

    def test_superuser_can_delete_public_post(self):
        self.assertTrue(self.public_post.can_delete(self.superuser))

    def test_anonymous_user_cannot_edite_public_post(self):
        self.assertFalse(self.public_post.can_edit(self.anonymous_user))

    def test_authenticated_user_cannot_edite_public_post(self):
        self.assertFalse(self.public_post.can_edit(self.some_user))

    # TODO
    def test__user_can_edite_public_post(self):
        self.assertTrue(self.public_post.can_edit(self.public_post.user))

    def test_superuser_can_edite_public_post(self):
        self.assertTrue(self.public_post.can_edit(self.superuser))

    def test_inactive_user_cannot_edit_post(self):

        self.public_post.user.is_active = False
        self.public_post.user.save()

        self.assertFalse(self.public_post.can_edit(self.public_post.user))

    def test_anonymous_user_cannot_edit_closed_topic(self):
        self.public_post.topic.close()

        self.assertFalse(self.public_post.can_edit(self.anonymous_user))

    def test_authenticated_user_cannot_edit_closed_topic(self):
        self.public_post.topic.close()

        self.assertFalse(self.public_post.can_edit(self.some_user))

    # TODO
    def test__user_cannot_edit_closed_topic(self):
        self.public_post.topic.close()

        self.assertFalse(self.public_post.can_edit(self.public_post.user))

    def test_superuser_can_edit_closed_topic(self):
        self.public_post.topic.close()

        self.assertTrue(self.public_post.can_edit(self.superuser))

    def test_anonymous_user_cannot_edit_expired_topic(self):
        self.public_post.created = timezone.now() - timedelta(seconds=(FORUM_EDIT_TIMEOUT * 60 + 1))
        self.public_post.save()

        self.assertFalse(self.public_post.can_edit(self.anonymous_user))

    def test_authenticated_user_cannot_edit_expired_topic(self):
        self.public_post.created = timezone.now() - timedelta(seconds=(FORUM_EDIT_TIMEOUT * 60 + 1))
        self.public_post.save()

        self.assertFalse(self.public_post.can_edit(self.some_user))

    # TODO
    def test__user_cannot_edit_expired_topic(self):
        self.public_post.created = timezone.now() - timedelta(seconds=(FORUM_EDIT_TIMEOUT * 60 + 1))
        self.public_post.save()

        self.assertFalse(self.public_post.can_edit(self.public_post.user))

    def test_superuser_can_edit_expired_topic(self):
        self.public_post.created = timezone.now() - timedelta(seconds=(FORUM_EDIT_TIMEOUT * 60 + 1))
        self.public_post.save()

        self.assertTrue(self.public_post.can_edit(self.superuser))

    # TODO
    def test_expired(self):
        self.public_post.created = timezone.now() - timedelta(seconds=(FORUM_EDIT_TIMEOUT * 60 + 1))
        self.public_post.save()

        self.assertTrue(self.public_post.expired)

    # TODO
    def test_topic_updates(self):

        updated = timezone.now() + timedelta(days=1)

        self.assertNotEqual(self.public_post.topic.updated, updated)

        self.public_post.updated = updated
        self.public_post.save()

        self.assertEqual(self.public_post.topic.updated, updated)


class TopicTest(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super(TopicTest, cls).setUpTestData()

        cls.public_topic = TopicFactory()
        cls.private_topic = TopicFactory()
        cls.private_topic.forum.category.groups.add(cls.group)

        # we do not track this for anonymous user, so just test API
        cls.topic = TopicFactory()

        for _ in range(3):
            PostFactory(topic=cls.topic)

    def setUp(self):
        self.public_topic.refresh_from_db()
        self.topic.refresh_from_db()

    def test_get_absolute_url(self):
        self.assertTrue(self.public_topic.get_absolute_url())

    def test_anonymous_user_has_access_to_public_topic(self):
        self.assertTrue(self.public_topic.has_access(self.anonymous_user))

    def test_authenticated_user_has_access_to_public_topic(self):
        self.assertTrue(self.public_topic.has_access(self.some_user))

    def test_group_user_has_access_to_public_topic(self):
        self.assertTrue(self.public_topic.has_access(self.group_user))

    def test_superuser_user_has_access_to_public_topic(self):
        self.assertTrue(self.public_topic.has_access(self.superuser))

    def test_anonymous_user_has_no_access_to_private_topic(self):
        self.assertFalse(self.private_topic.has_access(self.anonymous_user))

    def test_authenticated_user_has_no_access_to_private_topic(self):
        self.assertFalse(self.private_topic.has_access(self.some_user))

    def test_group_user_has_access_to_private_topic(self):
        self.assertTrue(self.private_topic.has_access(self.group_user))

    def test_superuser_user_has_access_to_private_topic(self):
        self.assertTrue(self.private_topic.has_access(self.superuser))

    def test_default_heresy(self):
        self.assertFalse(self.public_topic.heresy)

    def test_mark_heresy(self):

        self.public_topic.mark_heresy()
        self.assertTrue(self.public_topic.heresy)

    def test_unmark_heresy(self):

        self.public_topic.unmark_heresy()
        self.assertFalse(self.public_topic.heresy)

    def test_default_sticky(self):
        self.assertFalse(self.public_topic.sticky)

    def test_set_sticky(self):

        self.public_topic.stick()
        self.assertTrue(self.public_topic.sticky)

    def test_unstick(self):
        self.public_topic.unstick()
        self.assertFalse(self.public_topic.sticky)

    def test_default_closed(self):
        self.assertFalse(self.public_topic.closed)

    def test_close_topic(self):

        self.public_topic.close()
        self.assertTrue(self.public_topic.closed)

    def test_open_topic(self):
        self.public_topic.open()
        self.assertFalse(self.public_topic.closed)

    def test_anonymous_user_cannot_delete_public_topic(self):
        self.assertFalse(self.public_topic.can_delete(self.anonymous_user))

    def test_authenticated_user_cannot_delete_public_topic(self):
        self.assertFalse(self.public_topic.can_delete(self.some_user))

    def test_group_user_cannot_delete_private_topic(self): # XXX private
        self.assertFalse(self.private_topic.can_delete(self.group_user))

    def test_superuser_can_delete_public_topic(self):
        self.assertTrue(self.public_topic.can_delete(self.superuser))

    def test_anonymous_user_cannot_edite_public_post(self):
        self.assertFalse(self.public_topic.can_edit(self.anonymous_user))

    def test_authenticated_user_cannot_edite_public_post(self):
        self.assertFalse(self.public_topic.can_edit(self.some_user))

    def test_group_user_can_edite_public_post(self): # XXX private
        self.assertFalse(self.private_topic.can_edit(self.group_user))

    def test_superuser_can_edite_public_post(self):
        self.assertTrue(self.public_topic.can_edit(self.superuser))

    def test_anonymous_user_cannot_to_post(self):
        self.assertFalse(self.public_topic.can_post(self.anonymous_user))

    def test_authenticated_user_can_to_post(self):
        self.assertTrue(self.public_topic.can_post(self.some_user))

    def test_group_user_can_to_post(self):
        self.assertTrue(self.public_topic.can_post(self.group_user))

    def test_superuser_can_to_post(self):
        self.assertTrue(self.public_topic.can_post(self.superuser))

    def test_anonymous_user_cannot_to_post_in_closed_topic(self):

        self.public_topic.close()
        self.assertFalse(self.public_topic.can_post(self.anonymous_user))

    def test_authenticated_user_cannot_to_post_in_closed_topic(self):

        self.public_topic.close()
        self.assertFalse(self.public_topic.can_post(self.some_user))

    def test_group_user_cannot_to_post_in_closed_topic(self):

        self.public_topic.close()
        self.assertFalse(self.public_topic.can_post(self.group_user))

    def test_superuser_cannot_to_post_in_closed_topic(self):

        self.public_topic.close()
        self.assertFalse(self.public_topic.can_post(self.superuser))

    def test_anonymous_user_cannot_to_post_in_private_topic(self):
        self.assertFalse(self.private_topic.can_post(self.anonymous_user))

    def test_authenticated_user_cannot_to_post_in_private_topic(self):
        self.assertFalse(self.private_topic.can_post(self.some_user))

    def test_group_user_cannot_to_post_in_private_topic(self):
        self.assertTrue(self.private_topic.can_post(self.group_user))

    def test_superuser_cannot_to_post_in_private_topic(self):
        self.assertTrue(self.private_topic.can_post(self.superuser))

    def test_has_unread_if_user_is_anonymous(self):
        self.assertFalse(self.topic.has_unread(self.anonymous_user))

    def test_has_unread_if_user_is_authenticated(self):
        self.assertTrue(self.topic.has_unread(self.some_user))

    def test_has_unread_if_user_is_group_user(self):
        self.assertTrue(self.topic.has_unread(self.group_user))

    def test_has_unread_if_user_is_authenticated_and_if_topic_is_visited(self):
        self.topic.mark_visited_for(self.some_user)

        self.assertFalse(self.topic.has_unread(self.some_user))
        self.assertTrue(self.topic.has_unread(self.group_user))

    def test_has_unread_if_user_is_authenticated_and_new_post_created(self):
        # FIXME: sleep is a crap, but MySQL does not save milliseconds, so visit time and new post time are equal
        sleep(1)
        PostFactory(topic=self.topic)
        self.assertTrue(self.topic.has_unread(self.some_user))

    def test_has_unread_if_user_is_group_user_and_new_post_created(self):
        # FIXME: sleep is a crap, but MySQL does not save milliseconds, so visit time and new post time are equal
        sleep(1)
        PostFactory(topic=self.topic)
        self.assertTrue(self.topic.has_unread(self.group_user))

    def test_has_unread_if_forum_is_was_read(self):
        self.topic.forum.mark_read(self.some_user)

        self.assertFalse(self.topic.has_unread(self.some_user))
        self.assertTrue(self.topic.has_unread(self.group_user))

    # TODO
    def test_some_crap(self):
        self.topic.mark_visited_for(self.some_user)

        topic1 = TopicFactory(forum=self.topic.forum)
        self.assertTrue(topic1.has_unread(self.some_user))
        self.assertFalse(self.topic.has_unread(self.some_user))

        self.assertTrue(topic1.has_unread(self.group_user))
        self.assertTrue(self.topic.has_unread(self.group_user))

    def test_some_crap_2(self):
        topic1 = TopicFactory(forum=self.topic.forum)
        self.topic.forum.mark_read(self.some_user)
        self.assertFalse(topic1.has_unread(self.some_user))
        self.assertFalse(self.topic.has_unread(self.some_user))
        self.assertTrue(topic1.has_unread(self.group_user))
        self.assertTrue(self.topic.has_unread(self.group_user))

class TopicManagerTest(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super(TopicManagerTest, cls).setUpTestData()

        cls.public_forum = ForumFactory()
        cls.private_forum = ForumFactory()
        cls.private_forum.category.groups.add(cls.group)

        cls.pubic_topic = TopicFactory(forum=cls.public_forum)
        cls.private_topic = TopicFactory(forum=cls.private_forum)

    def test_unread_for_forum_with_authenticated_user_and_public_forum(self):

        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.some_user, self.public_forum)),
            [self.pubic_topic]
        )

    def test_unread_for_forum_with_authenticated_user_and_private_forum(self):
        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.some_user, self.private_forum)),
            []
        )

    def test_unread_for_forum_with_group_user_and_public_forum(self):

        self.assertEqual(list(Topic.objects.unread_for_forum(self.group_user, self.public_forum)),
            [self.pubic_topic]
        )

    def test_unread_for_forum_with_group_user_and_private_forum(self):
        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.group_user, self.private_forum)),
            [self.private_topic]
        )

    def test_unread_for_forum_with_superser_and_public_forum(self):
        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.superuser, self.public_forum)),
            [self.pubic_topic]
        )

    def test_unread_for_forum_with_superser_and_private_forum(self):
        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.superuser, self.private_forum)),
            [self.private_topic]
        )

    def test_unread_for_user(self):

        self.assertEqual(
            list(Topic.objects.unread(self.some_user)),
            [self.pubic_topic]
        )

    def test_unread_for_group_user(self):

        self.assertSequenceEqual(
            list(Topic.objects.unread(self.group_user)),
            [self.pubic_topic, self.private_topic]
        )

    def test_unread_for_superuser(self):

        self.assertSequenceEqual(
            list(Topic.objects.unread(self.superuser)),
            [self.pubic_topic, self.private_topic]
        )

    def test_unread_count_authenticated_user(self):
        self.assertEqual(Topic.objects.unread_count(self.some_user), 1)

    def test_unread_count_group_user(self):
        self.assertEqual(Topic.objects.unread_count(self.group_user), 2)

    def test_unread_count_superuser(self):
        self.assertEqual(Topic.objects.unread_count(self.superuser), 2)
