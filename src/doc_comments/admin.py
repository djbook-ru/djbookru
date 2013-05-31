# -*- coding: utf-8 -*-

from django.contrib import admin
from . import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ['created', 'comment', 'url', 'author', 'status']
    list_filter = ['status']

    def url(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_absolute_url(), obj.page_title)
    url.allow_tags = True

    def comment(self, obj):
        return obj.get_content()
    comment.allow_tags = True

admin.site.register(models.Comment, CommentAdmin)
