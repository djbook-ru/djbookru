from .models import Video
from django import forms
from django.utils.translation import ugettext_lazy as _
import oembed


class VideoAdminForm(forms.ModelForm):

    class Meta:
        model = Video

    def clean_video(self):
        video_link = self.cleaned_data.get('video')

        if video_link:
            try:
                oembed.site.embed(video_link)
            except oembed.exceptions.OEmbedException:
                raise forms.ValidationError(_(u'Incorrect video URL'))

        return video_link
