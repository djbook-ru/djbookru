from django.db import models
from django.utils.translation import ugettext_lazy as _

class News(models.Model):
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'))
    created = models.DateTimeField(_(u'created'), auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('news:news', [self.pk], {})