# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import markdown

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db import connection, models
from django.db.models import Q, F
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from src.forum.settings import FORUM_EDIT_TIMEOUT, POSTS_ON_PAGE
from src.utils.mail import send_templated_email
from src.utils.urlize import urlize


class CategoryManager(models.Manager):
    # TODO: Make queryset, so you can use this with more complex queries
    def for_user(self, user):
        qs = super(CategoryManager, self).get_queryset()

        if user.is_superuser and user.is_active:
            return qs
        elif user.is_authenticated():
            return qs.filter(Q(groups=None) | Q(groups__user=user))
        else:
            return qs.filter(groups=None)


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=80)
    groups = models.ManyToManyField(
        Group, blank=True, verbose_name=_('Groups'), related_name='forum_categories',
        help_text=_('Only users from these groups can see this category'))
    position = models.IntegerField(_('Position'), default=0)

    objects = CategoryManager()

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
            if user.is_active and user.is_superuser:
                return True

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

    def has_access(self, user):
        return self.category.has_access(user)

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
            return False

        visits_qs = Visit.objects.filter(user=user, topic__forum=self)

        if visits_qs.count() < self.topics.all().count():
            return True

        return visits_qs.filter(time__lt=models.F('topic__updated')).exists()

    def mark_read(self, user):
        if not user.is_authenticated():
            return

        now = timezone.now()
        unread_topics = Topic.objects.unread_for_forum(user, self)
        unread_ids = [obj.pk for obj in unread_topics]

        # update visits
        Visit.objects.filter(topic__id__in=unread_ids, user=user).update(time=now)

        # create visits that does not exist
        visits = []
        topics_to_visit = Topic.objects.filter(pk__in=unread_ids).exclude(visit__user=user)
        for topic in topics_to_visit:
            visits.append(Visit(user=user, topic=topic, time=now))
        Visit.objects.bulk_create(visits)


class Visit(models.Model):
    user = models.ForeignKey('accounts.User', verbose_name=_('user'), related_name='forum_visits')
    topic = models.ForeignKey('Topic', verbose_name=_('topic'))
    time = models.DateTimeField(_('time'), default=timezone.now)

    class Meta:
        unique_together = ('user', 'topic')


class TopicManager(models.Manager):

    def unread_for_forum(self, user, forum):

        """
        Возвращает непрочитанные переданным пользователем темы на переданном форуме.
        """

        # return user unread topics for forum
        if not forum.has_access(user):
            return Topic.objects.none()

        query = '''SELECT ft.* FROM forum_topic ft LEFT JOIN forum_visit fv ON ft.id = fv.topic_id AND fv.user_id = %s
WHERE ft.forum_id = %s AND (fv.time IS NULL OR fv.time < ft.updated);'''
        return self.raw(query, [user.pk, forum.pk])

    def unread(self, user):

        """
        Возвращает непрочитанные пользователем темы.
        """

        category_ids = Category.objects.for_user(user).values_list('pk', flat=True)

        if not category_ids:
            return []

        category_ids = ', '.join(str(id) for id in category_ids)

        query = '''SELECT ft.* FROM forum_topic ft INNER JOIN forum_forum ff ON ft.forum_id = ff.id
LEFT JOIN forum_visit fv ON ft.id = fv.topic_id AND fv.user_id = %%s
WHERE ff.category_id IN (%s) AND (fv.time IS NULL OR fv.time < ft.updated);''' % category_ids

        return self.raw(query, [user.pk])

    def unread_count(self, user):

        """
        Возвращает количество непрочитанных переданным пользователем тем.
        """

        # return self.filter(Q(visit__time__lt=F('updated')) & Q(visit__user__id=user.pk), forum__category__id__in=category_ids).count()
        category_ids = Category.objects.for_user(user).values_list('pk', flat=True)

        if not category_ids:
            return 0

        category_ids = ', '.join(str(id) for id in category_ids)

        cursor = connection.cursor()

        query = '''
        SELECT COUNT(*)
        FROM forum_topic ft
            INNER JOIN forum_forum ff ON ft.forum_id = ff.id
            LEFT JOIN forum_visit fv ON ft.id = fv.topic_id AND fv.user_id = %%s
        WHERE ff.category_id IN (%s) AND (fv.time IS NULL OR fv.time < ft.updated);''' % category_ids

        cursor.execute(query, [user.pk])
        row = cursor.fetchone()

        return row[0]


class RatingMixin(object):

    def has_vote(self, user):
        return self.votes.filter(pk=user.pk).exists()

    def update_rating(self):
        # FIXME: Use signal on votes add/remove
        self.rating = self.votes.count()
        self.save()


class Topic(models.Model, RatingMixin):
    forum = models.ForeignKey(Forum, related_name='topics', verbose_name=_('forum'))
    name = models.CharField(_('subject'), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), default=timezone.now)
    user = models.ForeignKey('accounts.User', verbose_name=_('user'), related_name='forum_topics')
    views = models.IntegerField(_('views count'), default=0)
    sticky = models.BooleanField(_('sticky'), default=False)
    closed = models.BooleanField(_('closed'), default=False)
    heresy = models.BooleanField(_('heresy'), default=False)
    visited_by = models.ManyToManyField(
        'accounts.User', verbose_name='visited_by', blank=True, through=Visit,
        related_name='visited_topics')
    rating = models.IntegerField(_('rating'), default=0)
    votes = models.ManyToManyField(
        'accounts.User', verbose_name=_('votes'), related_name='voted_topics', editable=False)
    send_response = models.BooleanField(_('send response on email'), default=False)

    objects = TopicManager()

    class Meta:
        ordering = ['-sticky', '-updated']
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('forum:topic', [self.pk])

    def has_access(self, user):
        return self.forum.has_access(user)

    def search(self):
        try:
            content = self.posts.all()[:1].get().get_content()
        except Post.DoesNotExist:
            content = ''
        return dict(source=_('Forum'), title=self.name, desc=content)

    @property
    def reply_count(self):
        return self.posts.all().count() - 1

    def mark_heresy(self):
        self.heresy = True
        self.save()

    def unmark_heresy(self):
        self.heresy = False
        self.save()

    def stick(self):
        self.sticky = True
        self.save()

    def unstick(self):
        self.sticky = False
        self.save()

    def close(self):
        self.closed = True
        self.save()

    def open(self):
        self.closed = False
        self.save()

    def can_delete(self, user):
        return user.is_active and user.is_superuser

    def can_edit(self, user):
        return user.is_active and user.is_superuser

    def can_post(self, user):
        return self.has_access(user) and not self.closed and user.is_authenticated()

    def do_send_notification(self):
        return self.send_response and self.can_post(self.user) and self.user.is_valid_email

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
            return False

        return not Visit.objects.filter(user=user, topic=self, time__gte=self.updated).exists()

    def send_email_about_post(self, post):
        if not self.do_send_notification():
            return

        if post.user == self.user:
            return

        subject = _('New post for your topic "%(topic)s"') % {'topic': self}
        context = {
            'post': post
        }
        send_templated_email(
            self.user.email, subject,
            'djforum/email_new_post.html',
            context,
            fail_silently=settings.DEBUG
        )


class Post(models.Model, RatingMixin):
    topic = models.ForeignKey(Topic, related_name='posts', verbose_name=_('Topic'))
    user = models.ForeignKey('accounts.User', related_name='forum_posts', verbose_name=_('User'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True)
    updated_by = models.ForeignKey(
        'accounts.User', verbose_name=_('Updated by'), related_name='forum_updated_posts',
        blank=True, null=True)
    body = models.TextField(_('Message'))
    rating = models.IntegerField(_('rating'), default=0)
    votes = models.ManyToManyField('accounts.User', verbose_name=_('votes'),
                                   related_name='voted_posts', editable=False)

    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __unicode__(self):
        LIMIT = 50
        tail = len(self.body) > LIMIT and '...' or ''
        return self.body[:LIMIT] + tail or '...'

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
        topic_url = reverse('forum:topic', args=[self.topic.pk])
        posts = list(self.topic.posts.all())
        post_index = posts.index(self)

        if post_index <= POSTS_ON_PAGE:
            return topic_url + '#post-' + str(self.pk)
        else:
            url = '%s?page=%s#post-%s'
            page = post_index / POSTS_ON_PAGE + 1
            return url % (topic_url, page, str(self.pk))

    def get_content(self):
        return mark_safe(urlize(markdown.markdown(self.body, safe_mode='escape')))

    @property
    def expired(self):
        # If expired author can't edit post
        timeout = FORUM_EDIT_TIMEOUT * 60
        return timeout < (timezone.now() - self.created).seconds

    def can_edit(self, user):
        if not user.is_authenticated():
            return False

        if user.is_superuser:
            return True

        if self.expired:
            return False

        if not self.topic.forum.category.has_access(user):
            return False

        if self.topic.closed:
            return False

        return user.is_active and self.user == user

    def can_delete(self, user):
        return user.is_active and user.is_superuser

    def has_access(self, user):
        return self.topic.has_access(user)
