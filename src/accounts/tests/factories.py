# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import factory

from src.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    first_name = factory.Sequence(lambda i: 'first_name%s' % i)
    is_valid_email = True
    last_name = factory.Sequence(lambda i: 'last_name%s' % i)
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    username = factory.Sequence(lambda i: 'username%s' % i)

    class Meta:
        model = User
