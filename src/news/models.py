# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from src.accounts.models import User


class NewsManager(models.Manager):
    use_for_related_fields = True

    def approved(self):
        return self.get_query_set().exclude(approved=False)


class News(models.Model):
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'), help_text=_('Use Markdown and HTML'))
    created = models.DateTimeField(_(u'created'), auto_now_add=True)
    author = models.ForeignKey(User, editable=False)
    approved = models.BooleanField(_(u'approved'), default=True,
        help_text=_(u'Can be used for draft'))
    link = models.CharField(_(u'link to original'), blank=True, max_length=500)

    class Meta:
        ordering = ['-created']
        verbose_name = _(u'News')
        verbose_name_plural = _(u'News')

    objects = NewsManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news:news', [self.pk], {})

    def search(self):
        return dict(source=_(u'News'), title=self.title, desc=self.content)

    def get_next(self):
        try:
            return News.objects.all().filter(created__gt=self.created).exclude(pk=self.pk).order_by('created')[:1].get()
        except News.DoesNotExist:
            return

    def get_prev(self):
        try:
            return News.objects.all().filter(created__lt=self.created).exclude(pk=self.pk).order_by('-created')[:1].get()
        except News.DoesNotExist:
            return


class ResourceRSS(models.Model):
    title = models.CharField(max_length=255, verbose_name=_(u'title'))
    description = models.TextField(verbose_name=_(u'description'), blank=True)
    link = models.URLField(verbose_name=_(u'link'))
    is_active = models.BooleanField(verbose_name=_(u'active?'), default=True)
    sync_date = models.DateTimeField(verbose_name=_(u'last update'), null=True,
        blank=True, editable=False)
    news_author = models.ForeignKey(User, verbose_name=_(u'author'))
    approved_by_default = models.BooleanField(
        verbose_name=_(u'approved by default?'), default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'RSS source')
        verbose_name_plural = _(u'RSS sources')
