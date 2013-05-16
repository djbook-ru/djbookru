# -*- coding: utf-8 -*-

import hashlib
import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import UserManager as BaseUserManager, User as BaseUser
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .. utils.mail import send_templated_email

EMAIL_CONFIRMATION_DAYS = getattr(settings, 'EMAIL_CONFIRMATION_DAYS', 3)

BaseUser._meta.get_field('email')._unique = True
BaseUser._meta.get_field('email').blank = False


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, force_email_valid=False):
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

        user.set_password(password)
        user.is_valid_email = True
        user.save(using=self._db, send_email_confirmation=False)
        return user


class User(BaseUser):
    biography = models.TextField(_(u'biography'), blank=True)
    homepage = models.URLField(_(u'homepage'), verify_exists=False, blank=True)
    is_valid_email = models.BooleanField(_(u'is valid email?'), default=False)
    achievements = models.ManyToManyField('Achievement', verbose_name=_(u'achievements'), through='UserAchievement')
    signature = models.TextField(_('forum signature'), blank=True,  max_length=1024)

    lng = models.FloatField(_(u'longitude'), blank=True, null=True)
    lat = models.FloatField(_(u'latitude'), blank=True, null=True)

    # for notification
    last_comments_read = models.DateTimeField(_(u'last comments read'), default=timezone.now)
    last_doc_comments_read = models.DateTimeField(_(u'last doc. comments read'), default=timezone.now)

    objects = UserManager()

    class Meta:
        verbose_name = _(u'User')
        verbose_name_plural = _(u'Users')

    def get_position(self):
        if not self.lng is None and not self.lat is None:
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
        return 'http://www.gravatar.com/avatar/%s.jpg?d=wavatar' % self.getMD5()

    def avatar(self):
        return self.gravatar_photo()

    def getMD5(self):
        m = hashlib.md5()
        m.update(self.user.email or self.user.username + '@djbook.ru')
        return m.hexdigest()

    @property
    def nickname(self):
        #for easy change of user name display
        return self.username

    @property
    def has_achievements(self):
        return self.achievements.exists()


def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = User(**values)
        user.save()

post_save.connect(create_custom_user, BaseUser)


class Announcement(models.Model):
    title = models.CharField(_(u'title'), max_length=300)
    link = models.URLField(_(u'link'), blank=True)
    content = models.TextField(_(u'content'), help_text=_('Use Markdown and HTML'))
    is_active = models.BooleanField(_(u'is active?'), default=True)
    created = models.DateTimeField(_(u'created'), auto_now_add=True)

    def __unicode__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    achievement = models.ForeignKey('Achievement', verbose_name=_(u'achievement'))
    note = models.TextField(_(u'note'), blank=True)

    class Meta:
        verbose_name = _(u'user achievement')
        verbose_name_plural = _(u'user achievements')
        unique_together = (('user', 'achievement'),)


class Achievement(models.Model):
    title = models.CharField(_(u'name'), max_length=500)
    description = models.TextField(_(u'description'), blank=True)
    active_icon = models.ImageField(_(u'active icon'), upload_to='uploads/Achievement/', help_text='http://mapicons.nicolasmollet.com/ #95ce4a')
    inactive_icon = models.ImageField(u'inactive icon', upload_to='uploads/Achievement/', help_text='http://mapicons.nicolasmollet.com/ #d5d5d5')

    class Meta:
        verbose_name = _(u'achievement')
        verbose_name_plural = _(u'achievements')

    def __unicode__(self):
        return self.title


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

        salt = sha_constructor(str(random.random()) + settings.SECRET_KEY).hexdigest()[:5]
        confirmation_key = sha_constructor(salt + user.email).hexdigest()
        try:
            current_site = Site.objects.get_current()
        except Site.DoesNotExist:
            return
        path = reverse("accounts:confirm_email", args=[confirmation_key])
        activate_url = u"http://%s%s" % (unicode(current_site.domain), path)
        context = {
            "user": user,
            "activate_url": activate_url,
            "current_site": current_site,
            "confirmation_key": confirmation_key,
        }
        subject = _(u'Please confirm your email address for %(site)s') % {'site': current_site.name}
        send_templated_email(user.email, subject, 'accounts/email_confirmation_message.html', context, fail_silently=settings.DEBUG)
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

    def __unicode__(self):
        return u"confirmation for %s" % self.user.email

    class Meta:
        verbose_name = _("e-mail confirmation")
        verbose_name_plural = _("e-mail confirmations")

    def key_expired(self):
        expiration_date = self.sent + timedelta(days=EMAIL_CONFIRMATION_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True
