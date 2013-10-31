# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class HeaderMessageAdmin(admin.ModelAdmin):
    list_display = ['message']

admin.site.register(models.HeaderMessage, HeaderMessageAdmin)
