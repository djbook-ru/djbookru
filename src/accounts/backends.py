from django.contrib.auth.backends import ModelBackend
from accounts.models import User

class CustomUserBackend(ModelBackend):
    
    def authenticate(self, username=None, password=None):
        print User.objects.all()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None