from .models import Topic, Post
from django import forms
from django.utils.translation import ugettext_lazy as _
from markitup.forms import MarkdownEditorMixin
from src.utils.forms import PlaceholderMixin


class AddPostForm(MarkdownEditorMixin, forms.ModelForm):

    class Meta:
        model = Post
        fields = ('body',)

    def __init__(self, topic, user, *args, **kwargs):
        self.topic = topic
        self.user = user
        super(AddPostForm, self).__init__(*args, **kwargs)

    def save(self):
        post = super(AddPostForm, self).save(commit=False)
        post.user = self.user
        post.topic = self.topic
        post.save()
        return post


class EditPostForm(MarkdownEditorMixin, forms.ModelForm):

    class Meta:
        model = Post
        fields = ('body',)


class AddTopicForm(PlaceholderMixin, MarkdownEditorMixin, forms.ModelForm):
    body = forms.CharField(label=_(u'Message'), widget=forms.Textarea)

    class Meta:
        model = Topic
        fields = ('name', 'body')

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
