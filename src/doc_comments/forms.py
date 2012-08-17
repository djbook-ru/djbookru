# -*- coding: utf-8 -*-

from django import forms

from . import models


class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ['content', 'page', 'xpath', 'page_title']
