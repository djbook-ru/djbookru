# -*- coding: utf-8 -*-

from django.db import models
import random


class Header_message(models.Model):
    message = models.CharField(u'Фраза', max_length=2048)
    weight = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ['-weight']
        verbose_name = u'Фраза'
        verbose_name_plural = u'Фразы'

    def __unicode__(self):
        return self.message

    @staticmethod
    def rnd():
        """
        return random message based on weight
        simple linear approach
        """
        if Header_message.objects.count() == 0:
            return None
        weights = Header_message.objects.all().order_by('-weight').values_list('id', 'weight')
        running_total = 0
        totals = []
        for w in weights:
            running_total += w[1]
            totals.append(running_total)
        rnd = random.random() * running_total
        for i, total in enumerate(totals):
            if rnd < total:
                rnd_id = weights[i][0]
                break

        return Header_message.objects.get(pk=rnd_id)
