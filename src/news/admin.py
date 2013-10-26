# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import TextField
from django.forms import ModelForm

from pagedown.widgets import AdminPagedownWidget
from src.news import models


class NewsForm(ModelForm):

    class Meta:
        model = models.News


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    search_fields = ('title',)
    form = NewsForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    formfield_overrides = {
        TextField: {'widget': AdminPagedownWidget},
    }
admin.site.register(models.News, NewsAdmin)
