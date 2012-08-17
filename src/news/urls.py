# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

from . import feeds

urlpatterns = patterns('src.news.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pk>\d+)/$', 'news', name='news'),
    (r'^feed/$', feeds.LatestNewsFeed()),
)
