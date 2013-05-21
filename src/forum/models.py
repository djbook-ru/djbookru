# -*- coding: utf-8 -*-

import os
import os.path

from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import urlize
from django.core.urlresolvers import reverse
from django.utils import timezone
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

    def has_unread(self, user):
        # Do not track for anonymous users
        if not user.is_authenticated():
            return True

        visits_qs = Visit.objects.filter(user=user, topic__forum=self)

        if visits_qs.count() < self.topics.all().count():
            return True

        return visits_qs.filter(time__lt=models.F('topic__updated')).exists()

    def mark_read(self, user):
        if not user.is_authenticated():
            return

        now = timezone.now()
        unread_topics = Topic.objects.unread(user, self)

        Visit.objects.filter(topic__id__in=[obj.pk for obj in unread_topics], user=user).update(time=now)

        visits = []

        for topic in Topic.objects.filter(pk__in=[obj.pk for obj in unread_topics]).exclude(visit__user=user):
            visits.append(Visit(user=user, topic=topic, time=now))

        Visit.objects.bulk_create(visits)

    def has_access(self, user):
        return self.category.has_access(user)


class Visit(models.Model):
    user = models.ForeignKey('accounts.User', verbose_name=_(u'user'), related_name='forum_visits')
    topic = models.ForeignKey('Topic', verbose_name=_(u'topic'))
    time = models.DateTimeField(_(u'time'), default=timezone.now)

    class Meta:
        unique_together = ('user', 'topic')


class TopicManager(models.Manager):

    def unread(self, user, forum):
        query = '''SELECT ft.* FROM forum_topic ft LEFT JOIN forum_visit fv ON ft.id = fv.topic_id AND fv.user_id = %s
WHERE ft.forum_id = %s AND (fv.time IS NULL or fv.time < ft.updated);'''
        return self.raw(query, [user.pk, forum.pk])


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics', verbose_name=_(u'forum'))
    name = models.CharField(_(u'subject'), max_length=255)
    created = models.DateTimeField(_(u'created'), auto_now_add=True)
    updated = models.DateTimeField(_(u'updated'), default=timezone.now)
    user = models.ForeignKey('accounts.User', verbose_name=_(u'user'), related_name='forum_topics')
    views = models.IntegerField(_(u'views count'), default=0)
    sticky = models.BooleanField(_(u'sticky'), default=False)
    closed = models.BooleanField(_(u'closed'), default=False)
    heresy = models.BooleanField(_(u'heresy'), default=False)
    visited_by = models.ManyToManyField('accounts.User', verbose_name='visited_by', blank=True,
                                        through=Visit, related_name='visited_topics')

    class Meta:
        ordering = ['-updated']
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    objects = TopicManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('forum:topic', [self.pk])

    @property
    def reply_count(self):
        return self.posts.all().count() - 1

    def can_delete(self, user):
        return user.is_active and user.is_superuser

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

    def mark_visited_for(self, user):
        if not user.is_authenticated():
            return None

        now = timezone.now()
        visit, created = Visit.objects.get_or_create(user=user, topic=self, defaults={
            'time': now
        })

        if not created:
            visit.time = now
            visit.save()

        return visit

    def has_unread(self, user):
        # Do not track for anonymous users
        if not user.is_authenticated():
            return True

        return not Visit.objects.filter(user=user, topic=self, time__gte=self.updated).exists()


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

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        self.topic.updated = self.updated or self.created
        self.topic.save()

    def delete(self):
        topic = self.topic
        super(Post, self).delete()
        if not topic.posts.exists():
            topic.delete()

    def get_absolute_url(self):
        return reverse('forum:topic', args=[self.topic.pk]) + '#post-' + str(self.pk)

    def get_content(self):
        return mark_safe(urlize(markdown.markdown(self.body, safe_mode='escape')))

    def can_edit(self, user):
        if not user.is_authenticated():
            return False

        if user.is_superuser:
            return True

        if not self.topic.forum.category.has_access(user):
            return False

        if self.topic.closed:
            return False

        return user.is_active and self.user == user

    def can_delete(self, user):
        return user.is_active and user.is_superuser
