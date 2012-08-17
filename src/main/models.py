# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson


class Book(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    created = models.DateTimeField(_(u'created'), auto_now_add=True)
    description = models.TextField(_(u'description'), blank=True)
    toc = models.TextField(_(u'ToC'), blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _(u'Book')
        verbose_name_plural = _(u'Books')

    def __unicode__(self):
        return self.name

    @classmethod
    def get(cls):
        try:
            return cls.objects.latest('created')
        except Book.DoesNotExist:
            return

    def get_toc(self):
        return simplejson.loads(self.toc)


class Page(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    slug = models.CharField(_(u'slug'), max_length=100)
    content = models.TextField(_(u'content'))
    book = models.ForeignKey(Book, related_name='pages', verbose_name=_(u'book'))
    chapter = models.CharField(_(u'chapter'), max_length=10, blank=True)
    section = models.CharField(_(u'section'), max_length=10, blank=True)

    class Meta:
        ordering = ['chapter', 'section']
        unique_together = ['slug', 'book']
        verbose_name = _(u'Page')
        verbose_name_plural = _(u'Pages')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('main:page', [self.slug])
