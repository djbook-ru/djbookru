# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms

from . import models


class CommentAdminForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ['content']


class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ['content', 'content_type', 'user', 'submit_date']
    search_fields = ('content',)

admin.site.register(models.Comment, CommentAdmin)
