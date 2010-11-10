from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User

class Category(models.Model):
    name = models.CharField(_(u'name'), max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('examples:category', [self.pk])

class Example(models.Model):
    category = models.ForeignKey(Category, related_name='examples', verbose_name=_(u'category'))
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'), help_text=_('Use Markdown and HTML'))
    created = models.DateTimeField(_(u'created'), auto_now=True)
    author = models.ForeignKey(User, editable=False)
    
    class Meta:
        verbose_name = _(u'Example')
        verbose_name_plural = _(u'Examples')
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('examples:detail', [self.pk])

