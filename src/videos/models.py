# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging_autocomplete.models import TagAutocompleteField


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

    @models.permalink
    def get_absolute_url(self):
        return ('videos:index',)
