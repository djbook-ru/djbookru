from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User

class News(models.Model):
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'), help_text=_('Use Markdown and HTML'))
    created = models.DateTimeField(_(u'created'), auto_now_add=True)
    author = models.ForeignKey(User, editable=False)
    
    class Meta:
        ordering = ['-created']
        verbose_name = _(u'News')
        verbose_name_plural = _(u'News')
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('news:news', [self.pk], {})  