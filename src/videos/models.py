from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging_autocomplete.models import TagAutocompleteField
import oembed


class Video(models.Model):
    title = models.CharField(_(u'title'), max_length=500)
    video = models.URLField(_(u'video URL'))
    description = models.TextField()
    tags = TagAutocompleteField(verbose_name=_(u'tags'))
    created = models.DateTimeField(_(u'created'), auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _(u'video')
        verbose_name_plural = _(u'videos')

    def __unicode__(self):
        return self.title

    def video_embed_code(self, maxwidth=300, maxheight=225):
        try:
            resource = oembed.site.embed(self.video, maxwidth=maxwidth, maxheight=maxheight)
            return resource.get_data()['html']
        except (oembed.exceptions.OEmbedException, KeyError):
            return ''

    def video_preview_code(self):
        try:
            resource = oembed.site.embed(self.video, maxwidth=260, maxheight=195)
            return resource.get_data()['html']
        except (oembed.exceptions.OEmbedException, KeyError):
            return ''
