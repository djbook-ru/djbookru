from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('examples:category', [self.pk])
    
class Example(models.Model):
    category = models.ForeignKey(Category, related_name='examples')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('examples:detail', [self.pk])
    