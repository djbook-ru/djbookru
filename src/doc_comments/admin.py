from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['page', 'xpath', 'author', 'created']

admin.site.register(Comment, CommentAdmin)
