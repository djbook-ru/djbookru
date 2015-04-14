# -*- coding: utf-8 -*-

from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import ugettext_lazy as _


class UserAchievementInline(admin.TabularInline):
    model = models.UserAchievement
    extra = 1


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = models.User
        fields = '__all__'


class UserRepositoryAdmin(admin.ModelAdmin):
    list_display = ('user', '__unicode__')
    list_filter = ('repo_type',)
    search_fields = ('user', 'user_name')


class UserRepositoryInline(admin.TabularInline):
    model = models.UserRepository
    fields = ('repo_type', 'user_name')


class CustomUserAdmin(UserAdmin):
    save_on_top = True
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_valid_email')
    list_filter = ('is_valid_email', 'is_staff', 'is_active', 'is_superuser')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        })
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'homepage', 'biography', 'signature',
                'lng', 'lat'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'is_valid_email', 'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    inlines = [UserAchievementInline, UserRepositoryInline]


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'link', 'is_active', 'created')
    list_filter = ('is_active',)


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'sent', 'is_valid_email')
    search_fields = ('user__username', 'user__email')

    def email(self, obj):
        return obj.user.email

    def is_valid_email(self, obj):
        return obj.user.is_valid_email
    is_valid_email.boolean = True


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)


admin.site.register(models.Announcement, AnnouncementAdmin)
admin.site.unregister(DjangoUser)
admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(models.Achievement, AchievementAdmin)
admin.site.register(models.UserRepository, UserRepositoryAdmin)
