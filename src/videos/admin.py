# -*- coding: utf-8 -*-

from django.contrib import admin

from . import forms
from . import models


class VideoAdmin(admin.ModelAdmin):
    form = forms.VideoAdminForm
    list_display = ['title', 'tags']

admin.site.register(models.Video, VideoAdmin)
