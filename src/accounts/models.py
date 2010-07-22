from django.contrib.auth.models import UserManager, User as BaseUser
from django.db import models

class User(BaseUser):
    
    objects = UserManager()