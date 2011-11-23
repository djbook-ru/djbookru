# encoding: utf-8

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from django.core.urlresolvers import reverse

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

class ExampleManager(models.Manager):
    use_for_related_fields = True

    def approved(self):
        return self.get_query_set().exclude(approved=False)

class Example(models.Model):
    category = models.ForeignKey(Category, related_name='examples', verbose_name=_(u'category'))
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'), help_text=_('Use <a target="blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown</a> and HTML'))
    created = models.DateTimeField(_(u'created'), auto_now=True)
    author = models.ForeignKey(User, editable=False)
    approved = models.BooleanField(_(u'approved'), default=True, help_text=_(u'Can be used for draft'))
    note = models.TextField(_(u'note'), blank=True, help_text=_(u'author\'s note, is not visible on site'))
    url = models.URLField(_(u'URL'), blank=True)
    topic_id = models.IntegerField(_(u'Topic ID'), default='0')

    class Meta:
        verbose_name = _(u'Example')
        verbose_name_plural = _(u'Examples')
        ordering = ('-created',)

    objects = ExampleManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('examples:detail', [self.pk])

    @models.permalink
    def get_edit_url(self):
        return ('admin:examples_example_change', [self.pk])

    @transaction.commit_on_success
    def save(self):
        from djangobb_forum.models import Forum, Topic, Post
        from accounts.models import User

        user = User.objects.get(username='rad')
        forum = Forum.objects.get(name='Обсуждение рецептов')

        topic = Topic(forum=forum, name=self.title, user=user)
        topic.save()

        self.topic_id = topic.pk

        super(Example, self).save()

        body_plain = u"""Обсуждение рецепта "%s" (http://djbook.ru%s)."""
        body_html = u"""Обсуждение рецепта &laquo;<a href="%s">%s</a>&raquo;."""
        title = self.title
        url = self.get_absolute_url()

        post = Post(topic=topic, user=user,
                    body=body_plain % (title, url),
                    body_html=body_html % (url, title))
        post.save()
