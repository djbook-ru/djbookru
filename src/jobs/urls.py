# -*- coding: utf-8 -*-
from django.conf.urls import url

from src.jobs.views import JobsListView, CompanyAllVacanciesListView, JobDetailView


urlpatterns = [
    url(r'^$', JobsListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', JobDetailView.as_view(), name="job_detail"),
    url(r'^company/(?P<company>[%a-z0-9]+)/$', CompanyAllVacanciesListView.as_view(),
        name='all_vacancies_company'),
    url(r'^add_position', 'src.jobs.views.add_position', name='add_position'),
    url(r'^edit_position/(?P<pk>\d+)/$', 'src.jobs.views.edit_position',
        name='edit_position'),
]
