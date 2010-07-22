from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import User as CustomUser

admin.site.unregister(User)    
admin.site.register(CustomUser, UserAdmin)