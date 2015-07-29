# -*- coding: utf-8 -*-
from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'src.jobs.views.index', name='index'),
]
