from django import forms
from .models import Comment


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