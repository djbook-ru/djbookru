# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from pagedown.widgets import PagedownWidget

from src.forum.models import Topic, Post
from src.utils.forms import PlaceholderMixin


class AddPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body': PagedownWidget(),
        }

    def __init__(self, topic, user, *args, **kwargs):
        self.topic = topic
        self.user = user
        super(AddPostForm, self).__init__(*args, **kwargs)

    def save(self):
        post = super(AddPostForm, self).save(commit=False)
        post.user = self.user
        post.topic = self.topic
        post.save()

        post.topic.send_email_about_post(post)

        return post


class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body': PagedownWidget(),
        }


class AddTopicForm(PlaceholderMixin, forms.ModelForm):
    body = forms.CharField(label=_('Message'), widget=PagedownWidget())

    class Meta:
        model = Topic
        fields = ('name', 'body', 'send_response')

    def __init__(self, forum, user, *args, **kwargs):
        self.forum = forum
        self.user = user
        super(AddTopicForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        topic = super(AddTopicForm, self).save(commit=False)
        topic.forum = self.forum
        topic.user = self.user
        topic.save()

        post = Post(topic=topic, user=self.user, body=data['body'])
        post.save()

        return topic


class MoveTopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('forum',)
