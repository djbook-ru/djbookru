# -*- coding: utf-8 -*-
from django.conf.urls import url

from src.jobs.views import JobsListView, CompanyAllVacanciesListView, JobDetailView


urlpatterns = [
    url(r'^$', JobsListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', JobDetailView.as_view(), name="job_detail"),
    url(r'^company/(?P<company>\w+)/$', CompanyAllVacanciesListView.as_view(),
        name='all_vacancies_company'),
    url(r'^vacancy_edit/(?P<pk>\d+)/$', 'src.jobs.views.vacancy_edit',
        name='vacancy_edit'),
]
