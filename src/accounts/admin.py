from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import User as CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'userrank', 'first_name', 'last_name', 'is_staff')    

admin.site.unregister(User)    
admin.site.register(CustomUser, CustomUserAdmin)