from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'page', 'author', 'created']

admin.site.register(Comment, CommentAdmin)
