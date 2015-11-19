# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import mail
from django.utils import timezone

from src.forum.models import Category, Topic, Post
from src.forum.tests.factories import CategoryFactory, ForumFactory, TopicFactory, PostFactory
from src.forum.settings import FORUM_EDIT_TIMEOUT
from .base import BaseTestCase


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

        # test superuser
        self.login(self.superuser)
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

        # test superuser
        self.login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 4)

        # TODO: add tests for users online

        # test with empty DB, this is common issue to ignore new installation with empty DB
        self.client.logout()
        Category.objects.all().delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 0)

    def test_forum(self):
        # test 404
        url = reverse('forum:forum', args=(123,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        public_forum = ForumFactory()
        for _ in range(3):
            TopicFactory(forum=public_forum)
        private_forum = ForumFactory()
        private_forum.category.groups.add(self.group)

        # test anonymous
        url = reverse('forum:forum', args=(public_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['forum'], public_forum)
        self.assertEqual(len(response.context['object_list']), 3)

        url = reverse('forum:forum', args=(private_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # test some_user
        self.login(self.some_user)
        url = reverse('forum:forum', args=(public_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:forum', args=(private_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # test group_user
        self.login(self.group_user)
        url = reverse('forum:forum', args=(public_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:forum', args=(private_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test superuser
        self.login(self.superuser)
        url = reverse('forum:forum', args=(public_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:forum', args=(private_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_topic(self):
        # test 404
        url = reverse('forum:topic', args=(123,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        public_topic = TopicFactory()
        private_topic = TopicFactory()
        private_topic.forum.category.groups.add(self.group)

        # test anonymous
        prev_views = public_topic.views
        url = reverse('forum:topic', args=(public_topic.pk,))
        response = self.client.get(url)
        public_topic.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['topic'], public_topic)
        self.assertEqual(response.context['form'], None)
        self.assertEqual(prev_views + 1, public_topic.views)

        url = reverse('forum:topic', args=(private_topic.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # test some_user
        self.login(self.some_user)
        prev_views = public_topic.views
        url = reverse('forum:topic', args=(public_topic.pk,))
        self.assertTrue(public_topic.has_unread(self.some_user))
        response = self.client.get(url)
        public_topic.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['form'], None)
        self.assertEqual(prev_views + 1, public_topic.views)
        self.assertFalse(public_topic.has_unread(self.some_user))

        public_topic.close()
        response = self.client.get(url)
        self.assertEqual(response.context['form'], None)
        public_topic.open()

        url = reverse('forum:topic', args=(private_topic.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # test group_user
        self.login(self.group_user)
        url = reverse('forum:topic', args=(public_topic.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:topic', args=(private_topic.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test superuser
        self.login(self.superuser)
        url = reverse('forum:topic', args=(public_topic.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:topic', args=(private_topic.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unread_topics(self):
        url = reverse('forum:unread_topics')

        # test anonymous
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test some_user
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)

        public_topic = TopicFactory()
        private_topic = TopicFactory()
        private_topic.forum.category.groups.add(self.group)

        response = self.client.get(url)
        self.assertEqual(list(response.context['object_list']), [public_topic])

        response = self.client.get(reverse('forum:mark_read_all'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(url)
        self.assertEqual(list(response.context['object_list']), [])

        # test group_user
        self.login(self.group_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['object_list']), [public_topic, private_topic])

        response = self.client.get(reverse('forum:mark_read_forum', args=(public_topic.forum.pk,)))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(url)
        self.assertEqual(list(response.context['object_list']), [private_topic])

        # test superuser
        self.login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['object_list']), [public_topic, private_topic])

    def test_my_topics(self):
        url = reverse('forum:my_topics')

        # test anonymous
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test some_user
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)

        topic = TopicFactory(user=self.some_user)
        for _ in range(3):
            TopicFactory()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['object_list']), [topic])

    def test_add_topic(self):
        public_forum = ForumFactory()
        private_forum = ForumFactory()
        private_forum.category.groups.add(self.group)

        # test anonymous
        url = reverse('forum:add_topic', args=(public_forum.pk,))
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test some user
        self.login(self.some_user)
        url = reverse('forum:add_topic', args=(private_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        self.assertFalse(public_forum.topics.exists())
        url = reverse('forum:add_topic', args=(public_forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'name': 'Topic name',
            'body': 'Topic body'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(public_forum.topics.count(), 1)
        new_topic = public_forum.topics.first()
        self.assertEqual(new_topic.name, data['name'])
        self.assertEqual(new_topic.posts.first().body, data['body'])

    def test_move_topic(self):
        forum1 = ForumFactory()
        forum2 = ForumFactory()
        topic = TopicFactory(user=self.some_user, forum=forum1)

        url = reverse('forum:move_topic', args=(topic.pk,))

        # test anonymous
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test some user
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # test superuser
        self.login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'forum': forum2.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        topic.refresh_from_db()
        self.assertEqual(topic.forum, forum2)

    def test_add_post(self):
        public_topic = TopicFactory()
        private_topic = TopicFactory()
        private_topic.forum.category.groups.add(self.group)

        data = {
            'body': 'Some post'
        }

        # test anonymous
        url = reverse('forum:add_post', args=(public_topic.pk,))
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))
        response = self.client.post(url, data)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test some user
        self.login(self.some_user)
        self.assertFalse(Post.objects.filter(topic=public_topic, user=self.some_user).exists())

        url = reverse('forum:add_post', args=(public_topic.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(topic=public_topic, user=self.some_user).exists())

        url = reverse('forum:add_post', args=(private_topic.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

        # test group user
        for user in (self.group_user, self.superuser):
            self.login(user)
            self.assertFalse(Post.objects.filter(topic=public_topic, user=user).exists())
            self.assertFalse(Post.objects.filter(topic=private_topic, user=user).exists())

            url = reverse('forum:add_post', args=(public_topic.pk,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Post.objects.filter(topic=public_topic, user=user).exists())

            url = reverse('forum:add_post', args=(private_topic.pk,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Post.objects.filter(topic=private_topic, user=user).exists())

    def _test_failed_post_edit(self, post):
        url = reverse('forum:edit_post', args=(post.pk,))

        data = {'body': 'New post%s' % timezone.now()}
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        post.refresh_from_db()
        self.assertNotEqual(post.body, data['body'])

    def test_edit_post(self):
        post = PostFactory(user=self.some_user)
        self.assertFalse(post.updated)
        self.assertFalse(post.updated_by)
        url = reverse('forum:edit_post', args=(post.pk,))
        data = {'body': 'New post'}

        # test anonymous
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))
        response = self.client.post(url, data)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test author edit
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        post.refresh_from_db()
        self.assertEqual(post.body, data['body'])
        self.assertEqual(post.updated_by, self.some_user)
        self.assertTrue(post.updated)

        # test other user
        self.login(self.group_user)
        self._test_failed_post_edit(post)

        # test closed
        self.login(self.some_user)
        post.topic.close()
        self._test_failed_post_edit(post)
        post.topic.open()

        # test expired
        post.created = timezone.now() - timedelta(seconds=(FORUM_EDIT_TIMEOUT * 60 + 1))
        post.save()
        self._test_failed_post_edit(post)

        # test superuser
        self.login(self.superuser)
        data = {'body': 'New post3'}
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        post.refresh_from_db()
        self.assertEqual(post.body, data['body'])
        self.assertEqual(post.updated_by, self.superuser)

    def test_subscribe_unsubscribe(self):
        self.some_user.is_valid_email = True
        self.some_user.save()
        topic = TopicFactory(user=self.some_user)
        self.assertFalse(topic.send_response)

        subscribe_url = reverse('forum:subscribe', args=(topic.pk,))
        unsubscribe_url = reverse('forum:unsubscribe', args=(topic.pk,))

        # test anonymous
        for url in (subscribe_url, unsubscribe_url):
            response = self.client.get(url)
            self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test other user
        self.login(self.group_user)
        for url in (subscribe_url, unsubscribe_url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        # test subscribe
        self.login(self.some_user)
        response = self.client.get(subscribe_url)
        self.assertEqual(response.status_code, 302)
        topic.refresh_from_db()
        self.assertTrue(topic.send_response)

        # test sending email
        mail.outbox = []
        url = reverse('forum:add_post', args=(topic.pk,))
        data = {'body': 'new post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mail.outbox, [])

        self.login(self.group_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

        mail.outbox = []
        self.some_user.is_valid_email = False
        self.some_user.save()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

        # test unsubscribe
        self.login(self.some_user)
        response = self.client.get(unsubscribe_url)
        self.assertEqual(response.status_code, 302)
        topic.refresh_from_db()
        self.assertFalse(topic.send_response)

        mail.outbox = []
        self.some_user.is_valid_email = True
        self.some_user.save()
        self.login(self.group_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

    def _test_topic_property_change(self, url_name, property):
        topic = TopicFactory(user=self.some_user)
        self.assertFalse(getattr(topic, property))
        url = reverse(url_name, args=(topic.pk,))

        # test anonymous
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test user
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        topic.refresh_from_db()
        self.assertFalse(getattr(topic, property))

        # test superuser
        self.login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        topic.refresh_from_db()
        self.assertTrue(getattr(topic, property))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        topic.refresh_from_db()
        self.assertFalse(getattr(topic, property))

    def test_heresy_unheresy_topic(self):
        self._test_topic_property_change('forum:heresy_unheresy_topic', 'heresy')

    def test_close_open_topic(self):
        self._test_topic_property_change('forum:close_open_topic', 'closed')

    def test_stick_unstick_topic(self):
        self._test_topic_property_change('forum:stick_unstick_topic', 'sticky')

    def test_delete_topic(self):
        topic = TopicFactory(user=self.some_user)
        url = reverse('forum:delete_topic', args=(topic.pk,))

        # test anonymous
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test user
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Topic.objects.filter(pk=topic.pk).exists())

        # test superuser
        self.login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(pk=topic.pk).exists())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(pk=topic.pk).exists())

    def test_delete_post(self):
        post = PostFactory(user=self.some_user)
        url = reverse('forum:delete_post', args=(post.pk,))

        # test anonymous
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (settings.LOGIN_URL, url))

        # test user
        self.login(self.some_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

        # test superuser
        self.login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def _test_vote(self, public_obj, private_obj, public_url, private_url):
        self.assertEqual(public_obj.rating, 0)
        self.assertEqual(private_obj.rating, 0)

        # test anonymous
        response = self.client.get(public_url)
        self.assertEqual(response.status_code, 403)
        response = self.client.get(private_url)
        self.assertEqual(response.status_code, 403)

        public_obj.refresh_from_db()
        private_obj.refresh_from_db()
        self.assertEqual(public_obj.rating, 0)
        self.assertEqual(private_obj.rating, 0)

        # test some user
        self.login(self.some_user)

        response = self.client.get(public_url)
        self.assertEqual(response.status_code, 200)
        public_obj.refresh_from_db()
        self.assertEqual(public_obj.rating, 1)

        response = self.client.get(public_url)
        self.assertEqual(response.status_code, 200)
        public_obj.refresh_from_db()
        self.assertEqual(public_obj.rating, 0)

        response = self.client.get(private_url)
        self.assertEqual(response.status_code, 403)
        public_obj.refresh_from_db()
        self.assertEqual(public_obj.rating, 0)

        # test group user
        self.login(self.group_user)

        response = self.client.get(private_url)
        self.assertEqual(response.status_code, 200)
        private_obj.refresh_from_db()
        self.assertEqual(private_obj.rating, 1)

        response = self.client.get(private_url)
        self.assertEqual(response.status_code, 200)
        private_obj.refresh_from_db()
        self.assertEqual(private_obj.rating, 0)

        # test superuser
        self.login(self.group_user)

        response = self.client.get(private_url)
        self.assertEqual(response.status_code, 200)
        private_obj.refresh_from_db()
        self.assertEqual(private_obj.rating, 1)

        response = self.client.get(private_url)
        self.assertEqual(response.status_code, 200)
        private_obj.refresh_from_db()
        self.assertEqual(private_obj.rating, 0)

    def test_vote_topic(self):
        public_topic = TopicFactory()
        private_topic = TopicFactory()
        private_topic.forum.category.groups.add(self.group)

        public_url = reverse('forum:vote_topic', args=(public_topic.pk,))
        private_url = reverse('forum:vote_topic', args=(private_topic.pk,))

        self._test_vote(public_topic, private_topic, public_url, private_url)

    def test_vote_post(self):
        public_post = PostFactory()
        private_post = PostFactory()
        private_post.topic.forum.category.groups.add(self.group)

        public_url = reverse('forum:vote_post', args=(public_post.pk,))
        private_url = reverse('forum:vote_post', args=(private_post.pk,))

        self._test_vote(public_post, private_post, public_url, private_url)

    def test_statistic(self):
        for _ in range(10):
            PostFactory()

        url = reverse('forum:statistic')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:posts_per_month_chart')
        # TODO OperationalError: near "from": syntax error
        # Предположительно возникает из-за используемой БД (sqlite)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_feeds(self):
        forum = ForumFactory()

        for _ in range(5):
            topic = TopicFactory(forum=forum)
            PostFactory(topic=topic)
            PostFactory(topic=topic)

        url = reverse('forum:feed_latest_forum_entries', args=(forum.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('forum:feed_latest_entries')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
