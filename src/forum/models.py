# -*- coding: utf-8 -*-

import os
import os.path

from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
import markdown


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=80)
    groups = models.ManyToManyField(Group, blank=True, verbose_name=_('Groups'),
        help_text=_('Only users from these groups can see this category'), related_name='forum_categories')
    position = models.IntegerField(_('Position'), default=0)

    class Meta:
        ordering = ['position']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('forum:index',)

    def has_access(self, user):
        if self.groups.count() > 0:
            if user.is_authenticated():
                try:
                    self.groups.get(user__pk=user.id)
                except Group.DoesNotExist:
                    return False
            else:
                return False
        return True


class Forum(models.Model):
    category = models.ForeignKey(Category, related_name='forums', verbose_name=_('Category'))
    name = models.CharField(_('Name'), max_length=80)
    position = models.IntegerField(_('Position'), default=0)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        ordering = ['position']
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('forum:forum', [self.pk])

    @property
    def topics_count(self):
        return Topic.objects.filter(forum=self).count()

    @property
    def posts_count(self):
        return Post.objects.filter(topic__forum=self).count()

    @property
    def last_post(self):
        try:
            return Post.objects.filter(topic__forum=self).order_by('-created')[:1].get()
        except Post.DoesNotExist:
            pass


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics', verbose_name=_('Forum'))
    name = models.CharField(_('Subject'), max_length=255)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True)
    user = models.ForeignKey('accounts.User', verbose_name=_('User'), related_name='forum_topics')
    views = models.IntegerField(_('Views count'), default=0)
    sticky = models.BooleanField(_('Sticky'), default=False)
    closed = models.BooleanField(_('Closed'), default=False)
    heresy = models.BooleanField(_('Heresy'), default=False)

    class Meta:
        ordering = ['-updated']
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('forum:topic', [self.pk])

    @property
    def replies_count(self):
        return self.posts.all().count() - 1

    def can_post(self, user):
        if not self.forum.category.has_access(user):
            return False

        if self.closed:
            return False

        return True

    @property
    def last_post(self):
        try:
            return Post.objects.filter(topic=self).order_by('-created')[:1].get()
        except Post.DoesNotExist:
            pass


class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts', verbose_name=_('Topic'))
    user = models.ForeignKey('accounts.User', related_name='forum_posts', verbose_name=_('User'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True)
    updated_by = models.ForeignKey('accounts.User', verbose_name=_('Updated by'), related_name='forum_updated_posts', blank=True, null=True)
    body = models.TextField(_('Message'))

    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __unicode__(self):
        LIMIT = 50
        tail = len(self.body) > LIMIT and '...' or ''
        return self.body[:LIMIT] + tail

    def get_absolute_url(self):
        return reverse('forum:topic', args=[self.topic.pk]) + '#post-' + str(self.pk)

    def get_content(self):
        return mark_safe(markdown.markdown(self.body, safe_mode='escape'))
