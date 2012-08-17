# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('src.videos.views',
    url(r'^$', 'index', name='index'),
)
