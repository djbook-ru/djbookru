# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

import micawber
from . import models


class VideoAdminForm(forms.ModelForm):

    class Meta:
        model = models.Video
        fields = '__all__'

    def clean_video(self):
        video_link = self.cleaned_data.get('video')

        if video_link:
            try:
                providers = micawber.bootstrap_basic()
                providers.request(video_link)
            except (micawber.exceptions.ProviderNotFoundException, micawber.exceptions.InvalidResponseException):
                raise forms.ValidationError(_(u'Incorrect video URL'))

        return video_link
