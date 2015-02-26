# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import TextField
from django.forms import ModelForm

from pagedown.widgets import AdminPagedownWidget
from src.news import models


class NewsForm(ModelForm):

    class Meta:
        model = models.News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'approved', 'created']
    search_fields = ('title',)
    form = NewsForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    formfield_overrides = {
        TextField: {'widget': AdminPagedownWidget},
    }


class ResourceRSSAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'is_active', 'approved_by_default', 'sync_date']

admin.site.register(models.News, NewsAdmin)
admin.site.register(models.ResourceRSS, ResourceRSSAdmin)
