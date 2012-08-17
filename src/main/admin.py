# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models
from . import forms


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    form = forms.BookAdminForm

admin.site.register(models.Book, BookAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'book', 'chapter', 'section']
    list_filter = ['book']
    search_fields = ('name', 'content')

admin.site.register(models.Page, PageAdmin)
