# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('src.claims.views',
    url(r'^$', 'index', name='index'),
)
