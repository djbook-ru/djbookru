# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

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

    def test_some_user_has_access_to_public_category(self):
        self.assertTrue(self.public_category.has_access(self.some_user))

    def test_group_user_has_access_to_public_category(self):
        self.assertTrue(self.public_category.has_access(self.group_user))

    def test_superuser_user_has_access_to_public_category(self):
        self.assertTrue(self.public_category.has_access(self.superuser))

    def test_anonymous_user_has_no_access_to_private_category(self):
        self.assertFalse(self.private_category.has_access(self.anonymous_user))

    def test_some_user_has_no_access_to_private_category(self):
        self.assertFalse(self.private_category.has_access(self.some_user))

    def test_group_user_has_access_to_private_category(self):
        self.assertTrue(self.private_category.has_access(self.group_user))

    def test_superuser_user_has_access_to_private_category(self):
        self.assertTrue(self.private_category.has_access(self.superuser))

    def test_anonymous_user_accessable_categories(self):
        self.assertSequenceEqual(list(Category.objects.for_user(self.anonymous_user)), [self.public_category])

    def test_some_user_accessable_categories(self):
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

    def test_get_absolute_url(self):
        self.assertTrue(self.public_forum.get_absolute_url())

    def test_anonymous_user_has_access_to_public_forum(self):
        self.assertTrue(self.public_forum.has_access(self.anonymous_user))

    def test_some_user_user_has_access_to_public_forum(self):
        self.assertTrue(self.public_forum.has_access(self.some_user))

    def test_group_user_user_has_access_to_public_forum(self):
        self.assertTrue(self.public_forum.has_access(self.group_user))

    def test_superuser_user_has_access_to_public_forum(self):
        self.assertTrue(self.public_forum.has_access(self.superuser))

    def test_anonymous_user_has_no_accesse_to_private_forum(self):
        self.assertFalse(self.private_forum.has_access(self.anonymous_user))

    def test_some_user_user_has_no_accesse_to_private_forum(self):
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

    def test_get_absolute_url(self):

        self.assertTrue(self.public_post.get_absolute_url())

    def test_post_is_expired(self):
        self.assertFalse(self.public_post.expired)

    def test_anonymous_user_has_access_to_public_post(self):
        self.assertTrue(self.public_post.has_access(self.anonymous_user))

    def test_some_user_user_has_access_to_public_post(self):
        self.assertTrue(self.public_post.has_access(self.some_user))

    def test_group_user_user_has_access_to_public_post(self):
        self.assertTrue(self.public_post.has_access(self.group_user))

    def test_superuser_user_has_access_to_public_post(self):
        self.assertTrue(self.public_post.has_access(self.superuser))

    def test_anonymous_user_has_no_accesse_to_private_post(self):
        self.assertFalse(self.private_post.has_access(self.anonymous_user))

    def test_some_user_user_has_no_accesse_to_private_post(self):
        self.assertFalse(self.private_post.has_access(self.some_user))

    def test_group_user_user_has_accesse_to_private_post(self):
        self.assertTrue(self.private_post.has_access(self.group_user))

    def test_superuser_user_has_accesse_to_private_post(self):
        self.assertTrue(self.private_post.has_access(self.superuser))

    def test_anonymous_user_cannot_delete_public_post(self):
        self.assertFalse(self.public_post.can_delete(self.anonymous_user))

    def test_some_user_cannot_delete_public_post(self):
        self.assertFalse(self.public_post.can_delete(self.some_user))

    def test_group_user_cannot_delete_private_post(self): # XXX private
        self.assertFalse(self.private_post.can_delete(self.group_user))

    def test_superuser_can_delete_public_post(self):
        self.assertTrue(self.public_post.can_delete(self.superuser))

    def test_anonymous_user_cannot_edite_public_post(self):
        self.assertFalse(self.public_post.can_edit(self.anonymous_user))

    def test_some_user_cannot_edite_public_post(self):
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

    def test_some_user_cannot_edit_closed_topic(self):
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

    def test_some_user_cannot_edit_expired_topic(self):
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

    def test_get_absolute_url(self):
        self.assertTrue(self.public_topic.get_absolute_url())

    def test_anonymous_user_has_access_to_public_topic(self):
        self.assertTrue(self.public_topic.has_access(self.anonymous_user))

    def test_some_user_has_access_to_public_topic(self):
        self.assertTrue(self.public_topic.has_access(self.some_user))

    def test_group_user_has_access_to_public_topic(self):
        self.assertTrue(self.public_topic.has_access(self.group_user))

    def test_superuser_user_has_access_to_public_topic(self):
        self.assertTrue(self.public_topic.has_access(self.superuser))

    def test_anonymous_user_has_no_access_to_private_topic(self):
        self.assertFalse(self.private_topic.has_access(self.anonymous_user))

    def test_some_user_has_no_access_to_private_topic(self):
        self.assertFalse(self.private_topic.has_access(self.some_user))

    def test_group_user_has_access_to_private_topic(self):
        self.assertTrue(self.private_topic.has_access(self.group_user))

    def test_superuser_user_has_access_to_private_topic(self):
        self.assertTrue(self.private_topic.has_access(self.superuser))

    def test_marks(self):

        self.assertFalse(self.public_topic.heresy)
        self.public_topic.mark_heresy()
        self.public_topic.refresh_from_db()
        self.assertTrue(self.public_topic.heresy)
        self.public_topic.unmark_heresy()
        self.public_topic.refresh_from_db()
        self.assertFalse(self.public_topic.heresy)

        self.assertFalse(self.public_topic.sticky)
        self.public_topic.stick()
        self.public_topic.refresh_from_db()
        self.assertTrue(self.public_topic.sticky)
        self.public_topic.unstick()
        self.public_topic.refresh_from_db()
        self.assertFalse(self.public_topic.sticky)

        self.assertFalse(self.public_topic.closed)
        self.public_topic.close()
        self.public_topic.refresh_from_db()
        self.assertTrue(self.public_topic.closed)
        self.public_topic.open()
        self.public_topic.refresh_from_db()
        self.assertFalse(self.public_topic.closed)

    def test_anonymous_user_cannot_delete_public_topic(self):
        self.assertFalse(self.public_topic.can_delete(self.anonymous_user))

    def test_some_user_cannot_delete_public_topic(self):
        self.assertFalse(self.public_topic.can_delete(self.some_user))

    def test_group_user_cannot_delete_private_topic(self): # XXX private
        self.assertFalse(self.private_topic.can_delete(self.group_user))

    def test_superuser_can_delete_public_topic(self):
        self.assertTrue(self.public_topic.can_delete(self.superuser))

    def test_anonymous_user_cannot_edite_public_post(self):
        self.assertFalse(self.public_topic.can_edit(self.anonymous_user))

    def test_some_user_cannot_edite_public_post(self):
        self.assertFalse(self.public_topic.can_edit(self.some_user))

    def test_group_user_can_edite_public_post(self): # TODO private
        self.assertFalse(self.private_topic.can_edit(self.group_user))

    def test_superuser_can_edite_public_post(self):
        self.assertTrue(self.public_topic.can_edit(self.superuser))

    def test_can_post(self):

        self.assertFalse(self.public_topic.can_post(self.anonymous_user))
        self.assertTrue(self.public_topic.can_post(self.some_user))
        self.assertTrue(self.public_topic.can_post(self.group_user))
        self.assertTrue(self.public_topic.can_post(self.superuser))
        self.public_topic.close()
        self.public_topic.refresh_from_db()
        self.assertFalse(self.public_topic.can_post(self.anonymous_user))
        self.assertFalse(self.public_topic.can_post(self.some_user))
        self.assertFalse(self.public_topic.can_post(self.group_user))
        self.assertFalse(self.public_topic.can_post(self.superuser))

        self.assertFalse(self.private_topic.can_post(self.anonymous_user))
        self.assertFalse(self.private_topic.can_post(self.some_user))
        self.assertTrue(self.private_topic.can_post(self.group_user))
        self.assertTrue(self.private_topic.can_post(self.superuser))

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

class TopicManagerTest(BaseTestCase):

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
            list(Topic.objects.unread_for_forum(self.superuser, public_forum)),
            [pubic_topic])
        self.assertEqual(
            list(Topic.objects.unread_for_forum(self.superuser, private_forum)),
            [private_topic])

        self.assertEqual(
            list(Topic.objects.unread(self.some_user)),
            [pubic_topic])
        self.assertEqual(
            list(Topic.objects.unread(self.group_user)),
            [pubic_topic, private_topic])
        self.assertEqual(
            list(Topic.objects.unread(self.superuser)),
            [pubic_topic, private_topic])

        self.assertEqual(Topic.objects.unread_count(self.some_user), 1)
        self.assertEqual(Topic.objects.unread_count(self.group_user), 2)
        self.assertEqual(Topic.objects.unread_count(self.superuser), 2)
