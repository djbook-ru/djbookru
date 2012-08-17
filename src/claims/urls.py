# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('src.claims.views',
    url(r'^$', 'index', name='index'),
)
