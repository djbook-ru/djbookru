# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import TextField
from django.forms import ModelForm

from ordered_model.admin import OrderedModelAdmin
from pagedown.widgets import AdminPagedownWidget

from src.examples import models


class CategoryAdmin(OrderedModelAdmin):
    list_display = ('name', 'move_up_down_links')


class ExampleForm(ModelForm):

    class Meta:
        model = models.Example
        exclude = ['is_draft_for']


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

    formfield_overrides = {
        TextField: {'widget': AdminPagedownWidget},
    }


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Example, ExampleAdmin)
