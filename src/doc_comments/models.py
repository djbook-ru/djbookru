from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from django.template.defaultfilters import linebreaksbr
from django.utils.http import urlquote


class Comment(models.Model):
    content = models.TextField(_(u'content'))
    author = models.ForeignKey(User, verbose_name=_('author'), related_name='doc_comments')
    page = models.CharField(_(u'path to page'), max_length=500)
    page_title = models.CharField(_(u'page title'), max_length=500)
    xpath = models.CharField(_(u'xpath'), max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _(u'comment')
        verbose_name_plural = _(u'comments')
        ordering = ['-created']

    def __unicode__(self):
        if len(self.content) > 50:
            return self.content[:50] + '...'
        return self.content

    def get_content(self):
        return linebreaksbr(self.content, autoescape=True)

    def get_absolute_url(self):
        return self.page + '?xpath=' + urlquote(self.xpath)
