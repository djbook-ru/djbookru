from django.db import models
from django.utils.translation import gettext_lazy as _

class Version(models.Model):
    name = models.CharField(_(u'Name'), max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class Page(models.Model):
    name = models.CharField(_(u'Name'), max_length=255)
    content = models.TextField()
    version = models.ForeignKey(Version)
    
    def __unicode__(self):
        return self.name    