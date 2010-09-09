# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import Book, Page
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from main.forms import BookAdminForm

class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    form = BookAdminForm

class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'book', 'chapter', 'section']
    list_filter = ['book']
    search_fields = ('name', 'content')
    
    class Media:
        js = [
            settings.ADMIN_MEDIA_PREFIX+'tinymce/jscripts/tiny_mce/tiny_mce.js', 
            'js/tinymce_setup.js'
        ]    
    
admin.site.register(Book, BookAdmin)
admin.site.register(Page, PageAdmin)