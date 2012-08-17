from django.contrib.auth.backends import ModelBackend
from accounts.models import User
from django.db.models import Q


class CustomUserBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
