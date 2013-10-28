# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

from . import feeds

urlpatterns = patterns('src.news.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pk>\d+)/$', 'news', name='news'),
    url(r'^(?P<pk>\d+)/edit/$', 'edit', name='edit'),
    url(r'^feed/$', feeds.LatestNewsFeed(), name='rss'),
)
