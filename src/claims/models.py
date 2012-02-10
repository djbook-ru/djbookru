# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

e = enumerate([_(u'New'), _(u'Assigned'), _(u'Fixed'), _(u'Invalid')], 1)
CLAIM_STATUSES = tuple([(x, y) for x,y in e])

class Claims(models.Model):
    ctx_left = models.CharField(verbose_name=_(u'Left Context Value'), max_length=255, blank=True)
    selected = models.CharField(verbose_name=_(u'Selected Text'), max_length=255)
    ctx_right = models.CharField(verbose_name=_(u'Right Context Value'), max_length=255, blank=True)
    status = models.IntegerField(verbose_name=_(u'Status of the Claim'), max_length=1, choices=CLAIM_STATUSES)
    status_applied = models.DateTimeField(verbose_name=_(u'Status Applied'), auto_now_add=True)
    comment = models.TextField(verbose_name=_(u'Reader\'s Comment'))
    reply = models.TextField(verbose_name=_(u'Enter here the reply for the Reader'), blank=True)
    url = models.URLField(verbose_name=_(u'Context URL'), verify_exists=False)
    email = models.EmailField(verbose_name=_(u'Reader\'s E-mail'))
    notify = models.BooleanField(verbose_name=_(u'Reader wants the Notify'))
    reg_datetime = models.DateTimeField(verbose_name=_(u'Registered'), auto_now_add=True)

    class Meta:
        verbose_name = _(u'Claim')
        verbose_name_plural = _(u'Claims')
        ordering=('-status_applied',)

    def __unicode__(self):
        return self.selected

    def save(self, *args, **kwargs):
        super(Claims, self).save(*args, **kwargs)
        self.sendemail()

    def sendemail(self):
        from django.core.mail import send_mail

        subject = '%s [%s]' % (unicode(_(u'DjangoBook in russian: Claim\'s state was changed to')),
                               unicode(self.get_status_display()))
        message = _(u'This is automatic generated message, you do not need to answer on it.')
        mail_from = '"%s" <%s>' % settings.ADMINS[0]
        recipient_list = ['"DjangoBook Reader" <%s>' % self.email, ]
        if self.reply is not None:
            message = _(u'%(auto)s\n\nThe reply on your comment is:\n%(reply)s') % {
                'auto': message,
                'reply': unicode(self.reply)
                }
        send_mail(subject.encode('utf-8'), message.encode('utf-8'), mail_from, recipient_list, fail_silently=True)

    @staticmethod
    def statistic():
        statuses = dict(CLAIM_STATUSES)
        css = ['', 'spelling_error_count_pending', 'spelling_error_count_assigned',
               'spelling_error_count_fixed', 'spelling_error_count_invalid']
        result = []
        for record in Claims.objects.values('status').annotate(count=Count('status')).order_by('status'):
            id = int(record['status'])
            result.append( {'title': statuses[id], 'count': record['count'], 'css': css[id],} )
        return result
        # [{'status': 4L, 'count': 5},
        #  {'status': 3L, 'count': 89},
        #  {'status': 2L, 'count': 7},
        #  {'status': 1L, 'count': 23}]
