# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import Book, Page
from main.forms import BookAdminForm


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    form = BookAdminForm


class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'book', 'chapter', 'section']
    list_filter = ['book']
    search_fields = ('name', 'content')

admin.site.register(Book, BookAdmin)
admin.site.register(Page, PageAdmin)
