from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from models import User as CustomUser, EmailConfirmation, UserAchievement, Achievement


class UserAchievementInline(admin.TabularInline):
    model = UserAchievement
    extra = 1


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser


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


class AchievementAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(EmailConfirmation)
