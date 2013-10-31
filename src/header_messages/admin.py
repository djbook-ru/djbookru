# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.db import models

from .models import HeaderMessage


class HeaderMessageAdmin(admin.ModelAdmin):
    list_display = ['message']
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea},
    }

admin.site.register(HeaderMessage, HeaderMessageAdmin)
