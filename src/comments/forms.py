# -*- coding: utf-8 -*-

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .. utils.forms import AjaxForm

from . import models


class CommentForm(forms.ModelForm, AjaxForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    content = forms.CharField(label=_('Comment'), widget=forms.Textarea,
                                    max_length=models.COMMENT_MAX_LENGTH)

    class Meta:
        model = models.Comment
        fields = ('content', 'reply_to', 'object_pk', 'content_type')

    def __init__(self, obj, *args, **kwargs):
        if obj:
            ct = ContentType.objects.get_for_model(obj)
            kwargs.setdefault('initial', {})
            kwargs['initial']['object_pk'] = obj.pk
            kwargs['initial']['content_type'] = ct.pk
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['reply_to'].widget = forms.HiddenInput()
        self.fields['object_pk'].widget = forms.HiddenInput()
        self.fields['content_type'].widget = forms.HiddenInput()

    def clean(self):
        reply_to = self.cleaned_data.get('reply_to')
        content_type = self.cleaned_data.get('content_type')
        object_pk = self.cleaned_data.get('object_pk')
        if reply_to and content_type and object_pk:
            if not reply_to.content_type == content_type and not reply_to.object_pk == object_pk:
                raise forms.ValidationError(_('You can reply to the comments of the same object only'))
        return self.cleaned_data

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value

    def save(self, user, commit=True):
        obj = super(CommentForm, self).save(False)
        obj.user = user
        if commit:
            obj.save()
        return obj

    def get_errors(self):
        from django.utils.encoding import force_unicode
        output = {}
        for key, value in self.errors.items():
            output[key] = '/n'.join([force_unicode(i) for i in value])
        return output
