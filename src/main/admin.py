# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms import ModelForm
from django.db.models import TextField
from pagedown.widgets import AdminPagedownWidget

from . import models
from . import forms


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    form = forms.BookAdminForm

admin.site.register(models.Book, BookAdmin)

class PageForm(ModelForm):
    
    class Meta:
        model = models.Page


class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ['name', 'book', 'chapter', 'section']
    list_filter = ['book']
    search_fields = ('name', 'content')
    
    formfield_overrides = {
        TextField: {'widget': AdminPagedownWidget},
    }

admin.site.register(models.Page, PageAdmin)
