from django.db import models
from django.utils.translation import ugettext_lazy as _
from .. accounts.models import User
import markdown


class Snipet(models.Model):
    LANGUAGE_CHOICES = (
        ('python', u'python'),
    )
    title = models.CharField(_(u'title'), max_length=255)
    description = models.TextField(_(u'description'), blank=True)
    language = models.CharField(_(u'language'), default='python', choices=LANGUAGE_CHOICES, max_length=100)
    author = models.ForeignKey(User, verbose_name=_(u'author'))
    created = models.DateTimeField(_(u'created'), auto_now_add=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('code_review:details', [self.pk], {})


class File(models.Model):
    name = models.CharField(_(u'name'), max_length=1000)
    content = models.TextField(_(u'content'))
    snipet = models.ForeignKey(Snipet)
    language = models.CharField(_(u'language'), default='python', max_length=100)

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    file = models.ForeignKey(File, verbose_name=_(u'file'))
    row = models.PositiveIntegerField(_(u'row'))
    content = models.TextField(_(u'comment'), max_length=1000)
    author = models.ForeignKey(User, verbose_name=_(u'author'), related_name='code_comments')
    created = models.DateTimeField(_(u'created'), auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u"%s: %s..." % (self.author, self.content[:50])

    def get_json(self):
        return {
            'id': self.pk,
            'row': self.row,
            'content': markdown.markdown(self.content),
            'author': unicode(self.author),
            'created': self.created,
            'author_avatar': self.author.avatar()
        }
