# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms import ModelForm
from markitup.forms import MarkdownEditorMixin
from . import models


class NewsForm(MarkdownEditorMixin, ModelForm):

    class Meta:
        model = models.News


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    form = NewsForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(models.News, NewsAdmin)
