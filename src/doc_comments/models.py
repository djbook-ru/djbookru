# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import linebreaksbr
from django.utils.http import urlquote

from .. accounts.models import User


class Comment(models.Model):
    NONE, ACCEPTED, CLOSED = 0, 1, 2
    STATUS_CHOICES = (
        (NONE, _(u'none')),
        (ACCEPTED, _(u'accepted')),
        (CLOSED, _(u'closed'))
    )
    content = models.TextField(_(u'content'))
    author = models.ForeignKey(User, verbose_name=_('author'), related_name='doc_comments')
    page = models.CharField(_(u'path to page'), max_length=500)
    page_title = models.CharField(_(u'page title'), max_length=500)
    xpath = models.CharField(_(u'xpath'), max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(_(u'status'), choices=STATUS_CHOICES, default=0)

    class Meta:
        verbose_name = _(u'doc. comment')
        verbose_name_plural = _(u'doc. comments')
        ordering = ['-created']

    def __unicode__(self):
        if len(self.content) > 50:
            return self.content[:50] + '...'
        return self.content

    def get_content(self):
        return linebreaksbr(self.content, autoescape=True)

    def get_absolute_url(self):
        return self.page + '?xpath=' + urlquote(self.xpath)

    @classmethod
    def get_reply_comments(cls, user):
        your_comments = cls.objects.filter(author=user)

        if not your_comments.exists():
            return cls.objects.none()

        f = None
        for c in your_comments:
            if f:
                f |= models.Q(page=c.page, xpath=c.xpath, created__gt=c.created)
            else:
                f = models.Q(page=c.page, xpath=c.xpath, created__gt=c.created)

        qs = cls.objects.filter(f).exclude(author=user)

        return qs
