# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = [
    url(r'^$', 'src.claims.views.index', name='index'),
]
