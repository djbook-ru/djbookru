# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from adzone.managers import AdManager


class Advertiser(models.Model):
    """
    A Model for our Advertiser.
    """

    company_name = models.CharField(_('Company Name'), max_length=255)
    website = models.URLField(_('Company Site'), verify_exists=(settings.DEBUG == False))
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _('Advertiser')
        verbose_name_plural = _('Advertisers')
        ordering = ('company_name',)

    def __unicode__(self):
        return self.company_name

    def get_website_url(self):
        return self.website


class AdCategory(models.Model):
    """
    a Model to hold the different Categories for adverts
    """
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class AdZone(models.Model):
    """
    a Model that describes the attributes and behaviours of ad zones
    """
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'))
    description = models.TextField(_('Description'))

    class Meta:
        verbose_name = _('Zone')
        verbose_name_plural = _('Zones')
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class AdBase(models.Model):
    """
    This is our base model, from which all ads will inherit.
    The manager methods for this model will determine which ads to
    display return etc.
    """
    title = models.CharField(_('Title'), max_length=255)
    url = models.URLField(_('Advertised URL'), verify_exists=(settings.DEBUG == False))
    enabled = models.BooleanField(_('Enabled'), default=False)
    since = models.DateTimeField(_('Since'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), editable=False, auto_now=True)

    # Relations
    advertiser = models.ForeignKey(Advertiser)
    category = models.ForeignKey(AdCategory)
    zone = models.ForeignKey(AdZone)

    # Our Custom Manager
    objects = AdManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('adzone_ad_view', [self.id])


class AdImpression(models.Model):
    """
    The AdImpression Model will record every time the ad is loaded on a page
    """
    impression_date = models.DateTimeField(_('When'), auto_now_add=True)
    source_ip = models.IPAddressField(_('Who'), null=True, blank=True)
    ad = models.ForeignKey(AdBase)

    class Meta:
        verbose_name = _('Ad Impression')
        verbose_name_plural = _('Ad Impressions')


class AdClick(models.Model):
    """
    The AdClick model will record every click that a add gets

    """
    click_date = models.DateTimeField(_('When'), auto_now_add=True)
    source_ip = models.IPAddressField(_('Who'), null=True, blank=True)
    ad = models.ForeignKey(AdBase)

    class Meta:
        verbose_name = _('Ad Click')
        verbose_name_plural = _('Ad Clicks')

    @staticmethod
    def by_period(start, end):
        qs = AdClick.objects.filter(click_date__gte=start, click_date__lt=end)
        qs = qs.extra(select={'day': "date_format(click_date, '%%Y-%%m-%%d')"})
        qs = qs.values('day', 'ad', 'ad__title').order_by()
        qs = qs.annotate(count=models.Count('ad'))

        out = []
        for base_id, base_title in dict(set(map(lambda x: (x['ad'], x['ad__title']), qs))).items():
            based_items = filter(lambda x: x['ad'] == base_id, qs)
            prepared_items = map(lambda x: (x['day'], x['count']), based_items)
            out.append((base_title, prepared_items))

        return out


class TextAd(AdBase):
    """ A most basic, text based advert """
    content = models.TextField(_('Content'))


class BannerAd(AdBase):
    """ A standard banner Ad """
    content = models.ImageField(_('Content'), upload_to="adzone/bannerads/")
