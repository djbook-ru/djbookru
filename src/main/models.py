from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import simplejson

class Book(models.Model):
    name = models.CharField(_(u'Name'), max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    toc = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created']
    
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get(cls):
        return cls.objects.latest('created')
    
    def get_toc(self):
        return simplejson.loads(self.toc)
    
class Page(models.Model):
    name = models.CharField(_(u'Name'), max_length=255)
    slug = models.CharField(max_length=100)
    content = models.TextField()
    book = models.ForeignKey(Book, related_name='pages')
    chapter = models.CharField(max_length=10, blank=True)
    section = models.CharField(max_length=10, blank=True)
    
    class Meta:
        unique_together = ['slug', 'book']
    
    def __unicode__(self):
        return self.name
    
    