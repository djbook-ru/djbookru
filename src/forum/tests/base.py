# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from src.accounts.tests.factories import UserFactory, GroupFactory


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.anonymous_user = AnonymousUser()
        cls.superuser = UserFactory(
            username='superuser', email='superuser@test.com', password='superuser',
            is_superuser=True)
        cls.some_user = UserFactory(username='user', email='user@test.com', password='user')
        cls.group_user = UserFactory(username='user1', email='user1@test.com', password='user1')
        cls.group = GroupFactory()
        cls.group_user.groups.add(cls.group)

    def login(self, user):
        # it is not a magic, just password is equal to username
        self.assertTrue(self.client.login(username=user.email, password=user.username))
