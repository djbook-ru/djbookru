# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class HeaderMessage(models.Model):
    message = models.CharField(_(u'Phrase'), max_length=2048)

    class Meta:
        verbose_name = _(u'Phrase')
        verbose_name_plural = _(u'Phrases')

    def __unicode__(self):
        if len(self.message) > 50:
            return self.message[:50] + "..."
        else:
            return self.message

    @staticmethod
    def random_message():
        try:
            return HeaderMessage.objects.order_by('?')[:1].get().message
        except HeaderMessage.DoesNotExist:
            return ""

