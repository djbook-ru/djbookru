# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import feeds

urlpatterns = patterns('src.news.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pk>\d+)/$', 'news', name='news'),
    url(r'^feed/$', feeds.LatestNewsFeed(), name='rss'),
)
