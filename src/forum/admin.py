# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from src.forum.models import Category, Forum, Topic, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    list_editable = ['position']


class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'position']
    list_editable = ['position']
    search_fields = ('name',)


class TopicAdmin(admin.ModelAdmin):
    list_filter = ['sticky', 'closed', 'heresy', 'send_response']
    list_display = ['name', 'forum', 'created', 'updated', 'user', 'views', 'rating', 'sticky',
                    'send_response']
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'topic', 'user', 'rating', 'created', 'updated', 'updated_by']
    search_fields = ('topic__name', 'body')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Topic, TopicAdmin)
