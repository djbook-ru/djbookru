# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from src.accounts.models import User


class JobsManager(models.Manager):
    use_for_related_fields = True

    def published_jobs(self):
        return self.get_queryset().exclude(status='DRT')

    def remote_work(self):
        return self.get_queryset().exclude(remote_work=True)


class Jobs(models.Model):
    # tuple variables for selecting the type of work
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    CONTRACT = 'CT'
    EMP_TYPE = (
        (FULL_TIME, _(u'Full Time')),
        (PART_TIME, _(u'Part Time')),
        (CONTRACT, _(u'Contract')),
    )

    # tuple variables for selecting the status position
    DRAFT = 'DRT'
    PUBLISHED = 'PUB'
    STATUS_POSITION = (
        (DRAFT, _(u'Draft')),
        (PUBLISHED, _(u'Published'))
    )
    employment_type = models.CharField(max_length=2,
                                       choices=EMP_TYPE,
                                       default=FULL_TIME,
                                       verbose_name=_(u'employment type'))
    location = models.CharField(max_length=255, verbose_name=_(u'location'))
    remote_work = models.BooleanField(default=False, verbose_name=_(u'remote work?'))
    author = models.ForeignKey(User, verbose_name=_(u'author'))
    title = models.CharField(max_length=255, verbose_name=_(u'job title'))
    description = models.TextField(verbose_name=_(u'job description'),
                                   help_text=_(u'Formatted with Markdown'))
    company_name = models.CharField(max_length=255, verbose_name=_(u'company name'))
    company_website = models.URLField(verbose_name=_(u'company website'),
                                      blank=True)
    how_to_apply = models.TextField(verbose_name=_(u'how to apply'),
                                    help_text=_(u'For example: Email your'
                                                u'resume to job@exmpl.com'))
    status = models.CharField(max_length=3,
                              verbose_name=_(u'status position'),
                              choices=STATUS_POSITION,
                              default=DRAFT)
    pub_date = models.DateField(auto_now_add=True)
    last_edit_date = models.DateField(auto_now=True)

    objects = JobsManager()

    class Meta(object):
        verbose_name = _(u'job')
        verbose_name_plural = _(u'jobs')
        ordering = ['-pub_date']

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('jobs:job_detail', args=[str(self.id)])

    def get_all_vacancies_company(self):
        # TODO: get rid of the gaps in the URL
        return reverse('jobs:all_vacancies_company', kwargs={'company': self.company_name.lower()})
