from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from django.core.exceptions import ValidationError


class PublishManager(Manager):
    def get_query_set(self):
        return super(PublishManager, self).get_query_set().filter(publish=True)


class Poll(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Title'), help_text=_('The parameter is used as question to user'))
    queue = models.ForeignKey('Queue', blank=True, null=True, verbose_name=_('Queue'), help_text=_('Do you want to use the poll as a stand alone poll or insert it into the queue?'))
    is_multiple = models.BooleanField(_(u'is multiple?'), default=False)
    startdate = models.DateField(verbose_name=_('Start date'), help_text=_('Must be unique'))
    publish = models.BooleanField(default=True, verbose_name=_('Publish'))
    votes = models.ManyToManyField('Vote', related_name='%(app_label)s_%(class)s_related', blank=True, verbose_name=_('Votes'), help_text=_('Choose variants of answers'))

    objects = models.Manager()
    publish_manager = PublishManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-startdate']
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')
        permissions = (("can_vote", _("User can vote")),)

    def clean(self):
        if self.queue is not None:
            err_msg = _('"Start dates" of polls in the same queue must be different')
            objs = Poll.objects.filter(queue=self.queue, startdate=self.startdate)
            count = objs.count()

            if count > 1:
                raise ValidationError(err_msg)
            elif count == 1:
                if objs[0] != self:
                    raise ValidationError(err_msg)

    def get_vote_count(self):
        return Vote.objects.filter(poll=self).count()
    vote_count = property(fget=get_vote_count)

    def get_cookie_name(self):
        return str('poll_%s' % (self.pk))


class Queue(models.Model):
    title = models.CharField(unique=True, max_length=250, verbose_name=_('Queue name'), help_text=_('It must be unique'))
    auth = models.BooleanField(verbose_name=_('Need auth?'), help_text=_('Do the poll queue is for authenticated users only or not? (If yes, users must have "can_vote" permission to vote)'))

    def __unicode__(self):
        if self.auth:
            auth = _('With auth')
        else:
            auth = _('Without auth')

        return '%s (%s)' % (self.title, auth)

    class Meta:
        ordering = ['-title']
        verbose_name = _('Queue')
        verbose_name_plural = _('Queues')


class Item(models.Model):
    poll = models.ForeignKey(Poll)
    userbox = models.BooleanField(verbose_name=_('Its userbox?'), help_text=_('Set it, if you want user to type its own answer. (show as textbox)'))
    value = models.CharField(max_length=250, verbose_name=_('Value'), help_text=_('Its a title of item'))
    index = models.SmallIntegerField(default='0', verbose_name=_('Position'), help_text=_('Its for positioning only'))

    def __unicode__(self):
        return '%s (%d)' % (self.value, self.index)

    class Meta:
        ordering = ['index']


class Vote(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_('Poll'))
    ip = models.IPAddressField(verbose_name=_('User\'s IP'))
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_('User'))
    datetime = models.DateTimeField(auto_now_add=True)
    choices = models.ManyToManyField(Item, through='Choice', verbose_name=_('Voited items'))

    def __unicode__(self):
        if isinstance(self.user, User):
            return self.user.username
        return self.ip

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')


class Choice(models.Model):
    vote = models.ForeignKey(Vote)
    item = models.ForeignKey(Item)
    uservalue = models.CharField(max_length=250, blank=True, null=True)
