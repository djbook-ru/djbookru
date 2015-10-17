# -*- coding: utf-8 -*-

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from src.forum.models import Forum, Topic, Post
from src.accounts.models import User
from ordered_model.models import OrderedModel


class Category(OrderedModel):
    name = models.CharField(_(u'name'), max_length=255)

    class Meta:
        ordering = ('order',)
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
        return self.get_queryset().exclude(approved=False)


class Example(models.Model):
    category = models.ForeignKey(Category, related_name='examples', verbose_name=_(u'category'))
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'), help_text=_(
        'Use <a target="blank" href="http://daringfireball.net/projects/'
        'markdown/syntax">Markdown</a> and HTML'))
    created = models.DateTimeField(_(u'created'), auto_now_add=True)
    author = models.ForeignKey(User)
    approved = models.BooleanField(
        _(u'approved'), default=True, help_text=_(u'Can be used for draft'))
    note = models.TextField(
        _(u'note'), blank=True, help_text=_(u'author\'s note, is not visible on site'))
    url = models.URLField(_(u'URL'), blank=True)
    topic_id = models.IntegerField(_(u'Topic ID'), default='0')
    is_draft_for = models.ForeignKey('self', verbose_name=_('is draft for'), blank=True, null=True)

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

    def get_next(self):
        try:
            return Example.objects.approved().filter(created__gt=self.created).exclude(pk=self.pk) \
                .order_by('created')[:1].get()
        except Example.DoesNotExist:
            return

    def get_prev(self):
        try:
            return Example.objects.approved().filter(created__lt=self.created).exclude(pk=self.pk) \
                .order_by('-created')[:1].get()
        except Example.DoesNotExist:
            return

    @models.permalink
    def get_edit_url(self):
        return ('admin:examples_example_change', [self.pk])

    @transaction.atomic
    def save(self):
        is_create = self.pk is None and not self.is_draft_for
        is_draft_apply = self.is_draft_for and self.approved

        if is_draft_apply:
            original = Example.objects.get(id=self.is_draft_for.id)
            original.title = self.title
            original.category = self.category
            original.content = self.content
            original.note = self.note
            original.save()
            self.delete()

        if is_create:
            user = self.author

            forum = Forum.objects.get(name=u'Обсуждение рецептов')
            topic = Topic(forum=forum, name=self.title, user=user)
            topic.save()

            self.topic_id = topic.pk

        if not is_draft_apply:
            super(Example, self).save()

        if is_create:
            body = u"""Обсуждение рецепта "%s" (http://djbook.ru%s)."""
            title = self.title
            url = self.get_absolute_url()

            post = Post(topic=topic, user=user,
                        body=body % (title, url))
            post.save()

    def search(self):
        return dict(source=_(u'Example'), title=self.title, desc=self.content)

    @property
    def topic(self):
        try:
            topic = Topic.objects.get(pk=self.topic_id)
        except Topic.DoesNotExist:
            topic = None

        return topic

    def can_edit(self, user):
        if not user.is_authenticated():
            return False

        if user.is_superuser:
            return True

        return user.is_active and self.author == user
