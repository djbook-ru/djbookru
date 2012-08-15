from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import User as CustomUser, EmailConfirmation, UserAchievement, Achievement


class UserAchievementInline(admin.TabularInline):
    model = UserAchievement
    extra = 1


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_valid_email', 'password')
    inlines = [UserAchievementInline]


class AchievementAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(EmailConfirmation)
