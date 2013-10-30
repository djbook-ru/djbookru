# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class Header_messageAdmin(admin.ModelAdmin):
    list_display = ['message', 'weight']

admin.site.register(models.Header_message, Header_messageAdmin)
