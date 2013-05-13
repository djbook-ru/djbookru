# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend

from . import models


class CustomUserBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            user = models.User.objects.get(email=username)
            if user.check_password(password):
                return user
        except models.User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return models.User.objects.get(pk=user_id)
        except models.User.DoesNotExist:
            return None
