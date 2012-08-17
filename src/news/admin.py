# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(models.News, NewsAdmin)
