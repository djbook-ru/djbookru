# -*- coding: utf-8 -*-

from . import models
from .. utils.admin import LogModelAdmin
from django.contrib import admin
from django.forms import ModelForm
from markitup.forms import MarkdownEditorMixin
from ordered_model.admin import OrderedModelAdmin


class CategoryAdmin(OrderedModelAdmin):
    list_display = ('name', 'move_up_down_links')


class ExampleForm(MarkdownEditorMixin, ModelForm):

    class Meta:
        model = models.Example


class ExampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'approved', 'created')
    list_filter = ('category', 'approved')
    raw_id_fields = ('author',)
    search_fields = ('title',)
    form = ExampleForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Example, ExampleAdmin)
