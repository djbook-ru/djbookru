# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import hashlib
import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import UserManager as BaseUserManager, User as BaseUser
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from src.utils.db.fields.country_field import CountryField
from src.utils.mail import send_templated_email

EMAIL_CONFIRMATION_DAYS = getattr(settings, 'EMAIL_CONFIRMATION_DAYS', 3)

BaseUser._meta.get_field('email')._unique = True
BaseUser._meta.get_field('email').blank = False


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, force_email_valid=False,
                    send_email_confirmation=True):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now)

        if force_email_valid:
            user.is_valid_email = True
            send_email_confirmation = False
            password = self.make_random_password()

            current_site = Site.objects.get_current()
            subject = _('You just created account on %(site)s') % {'site': current_site.name}

            context = {
                'email': user.email,
                'password': password,
                'current_site': current_site
            }
            send_templated_email(user.email, subject, 'accounts/email_new_user.html', context,
                                 fail_silently=settings.DEBUG)

        user.set_password(password)
        user.save(using=self._db, send_email_confirmation=send_email_confirmation)
        return user


class User(BaseUser):
    biography = models.TextField(_('biography'), blank=True)
    homepage = models.URLField(_('homepage'), blank=True)
    is_valid_email = models.BooleanField(_('is valid email?'), default=False)
    achievements = models.ManyToManyField(
        'Achievement', verbose_name=_('achievements'), through='UserAchievement')
    signature = models.TextField(_('forum signature'), blank=True, max_length=1024)
    location = models.CharField(max_length=64, blank=True)
    country = CountryField(blank=True)

    lng = models.FloatField(_('longitude'), blank=True, null=True)
    lat = models.FloatField(_('latitude'), blank=True, null=True)

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_position(self):
        if self.lng is not None and self.lat is not None:
            return {
                'lat': self.lat,
                'lng': self.lng,
                'url': self.get_absolute_url(),
                'username': unicode(self),
                'avatar': self.avatar()
            }

    def save(self, *args, **kwargs):
        send_confirmation = False

        if not self.email:
            self.is_valid_email = False
        elif self.pk:
            try:
                before_save = self.__class__._default_manager.get(pk=self.pk)
                send_confirmation = before_save.email != self.email
            except models.ObjectDoesNotExist:
                send_confirmation = True
        elif not self.is_valid_email:
            send_confirmation = True

        if send_confirmation:
            self.is_valid_email = False

        send_email_confirmation = kwargs.pop('send_email_confirmation', True)
        super(User, self).save(*args, **kwargs)

        if send_confirmation and send_email_confirmation:
            EmailConfirmation.objects.send_confirmation(self)

    @property
    def comments_count(self):
        if not hasattr(self, '_comments_count'):
            setattr(self, '_comments_count', self.comment_set.count())
        return self._comments_count

    @models.permalink
    def get_absolute_url(self):
        return ('accounts:profile', [self.pk])

    def gravatar_photo(self):
        return 'https://www.gravatar.com/avatar/%s.jpg?d=wavatar' % self.getMD5()

    def avatar(self):
        return self.gravatar_photo()

    def getMD5(self):
        m = hashlib.md5()
        m.update(self.user.email.encode('utf8') or self.user.username + '@djbook.ru')
        return m.hexdigest()

    @property
    def nickname(self):
        # for easy change of user name display
        return self.username

    @property
    def has_achievements(self):
        return self.achievements.exists()

    @property
    def forum_post_count(self):
        return self.forum_posts.count()

    @property
    def spammer(self):
        try:
            _ = Achievement.objects.get(
                userachievement__user=self, title=u'Спаммер')  # FIXME
        except Achievement.DoesNotExist:
            return False
        else:
            return True

    @spammer.setter
    def spammer(self, value):
        achievement = Achievement.objects.get(title=u'Спаммер')
        if value:
            UserAchievement.objects.create(
                user=self, achievement=achievement)
        else:
            UserAchievement.objects.filter(
                user=self, achievement=achievement).delete()


def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = User(**values)
        user.save()

post_save.connect(create_custom_user, BaseUser)


class Announcement(models.Model):
    title = models.CharField(_('title'), max_length=300)
    link = models.URLField(_('link'), blank=True)
    content = models.TextField(_('content'), help_text=_('Use Markdown and HTML'))
    is_active = models.BooleanField(_('is active?'), default=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        verbose_name = _('announcement')
        verbose_name_plural = _('announcements')

    def __unicode__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    achievement = models.ForeignKey('Achievement', verbose_name=_('achievement'))
    note = models.TextField(_('note'), blank=True)

    class Meta:
        verbose_name = _('user achievement')
        verbose_name_plural = _('user achievements')
        unique_together = (('user', 'achievement'),)


class Achievement(models.Model):
    title = models.CharField(_('name'), max_length=500)
    description = models.TextField(_('description'), blank=True)
    active_icon = models.ImageField(
        _('active icon'), upload_to='uploads/Achievement/',
        help_text='https://mapicons.nicolasmollet.com/ #95ce4a')
    inactive_icon = models.ImageField(
        'inactive icon', upload_to='uploads/Achievement/',
        help_text='https://mapicons.nicolasmollet.com/ #d5d5d5')

    class Meta:
        verbose_name = _('achievement')
        verbose_name_plural = _('achievements')

    def __unicode__(self):
        return self.title


class UserRepository(models.Model):
    # FIXME: User strings, so DB contains some readable data, not just 1 or 2
    GITHUB, BITBUCKET = 1, 2
    REPO_TYPE_CHOICES = (
        (GITHUB, 'GitHub'),
        (BITBUCKET, 'BitBucket')
    )
    REPO_URL_TEMPLATES = {
        GITHUB: 'https://github.com/{}/',
        BITBUCKET: 'https://bitbucket.org/{}/'
    }

    user = models.ForeignKey(User, verbose_name=_('user'))
    repo_type = models.PositiveIntegerField(_('type'), choices=REPO_TYPE_CHOICES)
    user_name = models.CharField(_('login'), max_length=64)

    class Meta:
        verbose_name = _('user repository')
        verbose_name_plural = _('user repositories')

    def __unicode__(self):
        return self.REPO_URL_TEMPLATES[self.repo_type].format(self.user_name)


class EmailConfirmationManager(models.Manager):

    def confirm_email(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None
        if not confirmation.key_expired():
            user = confirmation.user
            user.is_valid_email = True
            user.save()
            return user

    def send_confirmation(self, user):
        assert user.email

        self.filter(user=user).delete()

        salt = hashlib.sha1(str(random.random()) + settings.SECRET_KEY).hexdigest()[:5]
        confirmation_key = hashlib.sha1(salt + user.email.encode('utf8')).hexdigest()
        try:
            current_site = Site.objects.get_current()
        except Site.DoesNotExist:
            return
        path = reverse('accounts:confirm_email', args=[confirmation_key])
        activate_url = 'https://%s%s' % (unicode(current_site.domain), path)
        context = {
            'user': user,
            'activate_url': activate_url,
            'current_site': current_site,
            'confirmation_key': confirmation_key,
        }
        subject = _('Please confirm your email address for %(site)s') % {'site': current_site.name}
        send_templated_email(user.email, subject, 'accounts/email_confirmation_message.html',
                             context, fail_silently=settings.DEBUG)
        return self.create(
            user=user,
            sent=timezone.now(),
            confirmation_key=confirmation_key)

    def delete_expired_confirmations(self):
        d = timezone.now() - timedelta(days=EMAIL_CONFIRMATION_DAYS)
        self.filter(sent__lt=d).delete()


class EmailConfirmation(models.Model):
    user = models.ForeignKey(User)
    sent = models.DateTimeField()
    confirmation_key = models.CharField(max_length=40)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _('e-mail confirmation')
        verbose_name_plural = _('e-mail confirmations')

    def __unicode__(self):
        return 'confirmation for %s' % self.user.email

    def key_expired(self):
        expiration_date = self.sent + timedelta(days=EMAIL_CONFIRMATION_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True
