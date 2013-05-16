from django.db import models
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModel


class UsefulLink(OrderedModel):
    url = models.URLField(u'URL')
    name = models.CharField(_(u'name'), max_length=250)

    class Meta:
        verbose_name = _(u'useful link')
        verbose_name_plural = _(u'useful links')
        ordering = ('order',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url


class SourceCode(OrderedModel):
    url = models.URLField(u'URL')
    name = models.CharField(_(u'name'), max_length=250)

    class Meta:
        verbose_name = _(u'source code')
        verbose_name_plural = _(u'source codes')
        ordering = ('order',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url
