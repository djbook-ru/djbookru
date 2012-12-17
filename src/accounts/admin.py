# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import ugettext_lazy as _

from . import models


class UserAchievementInline(admin.TabularInline):
    model = models.UserAchievement
    extra = 1


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = models.User


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_valid_email', 'password')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'homepage', 'biography')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_valid_email',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [UserAchievementInline]


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'link', 'is_active', 'created')

admin.site.register(models.Announcement, AnnouncementAdmin)
admin.site.unregister(DjangoUser)
admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.EmailConfirmation)
