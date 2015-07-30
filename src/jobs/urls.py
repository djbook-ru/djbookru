# -*- coding: utf-8 -*-
from django.conf.urls import url

from src.jobs.views import JobsListView


urlpatterns = [
    url(r'^$', JobsListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', 'src.jobs.views.job_detail', name="job_detail"),
]
