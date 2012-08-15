from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import User as CustomUser, EmailConfirmation


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_valid_email', 'password')


admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmailConfirmation)
