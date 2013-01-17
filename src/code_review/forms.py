from django import forms
from django.forms.models import inlineformset_factory
from .models import Comment, Snipet, File

FileFormset = inlineformset_factory(Snipet, File,can_delete=False)


class AddSnipetForm(forms.ModelForm):

    class Meta:
        model = Snipet
        fields = ('title', 'description', 'language')

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super(AddSnipetForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(AddSnipetForm, self).save(commit=False)
        obj.author = self.author
        if commit:
            obj.save()
        return obj


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('row', 'content')

    def __init__(self, file_obj, author, *args, **kwargs):
        self.file = file_obj
        self.author = author
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(CommentForm, self).save(commit=False)
        obj.file = self.file
        obj.author = self.author
        if commit:
            obj.save()
        return obj
