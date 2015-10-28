# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from . import feeds

urlpatterns = patterns('src.examples.views',
    url(r'^$', 'index', name='index'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'detail', name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', 'edit', name='edit'),
    url(r'^c(?P<pk>\d+)/$', 'category', name='category'),
    url(r'^feed/$', feeds.LatestExamplesFeed(), name='rss'),
)
