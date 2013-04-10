# -*- coding: utf-8 -*-

import simplejson
from datetime import timedelta

from django.utils import timezone

from admin_tools.dashboard.modules import DashboardModule
from admin_tools.utils import AppListElementMixin
from report_tools import charts
from report_tools.chart_data import ChartData
from report_tools.renderers.googlecharts import GoogleChartsRenderer
from report_tools.reports import Report

from . import models


class AdClickReport(Report):
    renderer = GoogleChartsRenderer
    multiseries_line_chart = charts.LineChart(title="Last 30 days report", width="500")

    def get_data_for_multiseries_line_chart(self):
        data = ChartData()
        end = timezone.now().date()
        start = end - timedelta(days=30)
        titles, days = models.AdClick.by_period(start, end)

        data.add_column("Report Period")

        indexes = []
        for pk, title in titles:
            indexes.append(pk)
            data.add_column(title)

        for marker, dictval in days:
            data.add_row([marker] + [dictval.get(i, 0) for i in indexes])

        return data


class AdClickModule(DashboardModule, AppListElementMixin):
    u"""Clicks for last 30 days."""

    template = 'adzone/panel_clicks.html'
    models = None
    exclude = None
    include_list = None
    exclude_list = None

    def __init__(self, title=None, models=None, exclude=None, **kwargs):
        self.models = list(models or [])
        self.exclude = list(exclude or [])
        self.include_list = kwargs.pop('include_list', [])  # deprecated
        self.exclude_list = kwargs.pop('exclude_list', [])  # deprecated
        super(AdClickModule, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        if self._initialized:
            return

        self.children = AdClickReport()
        self._initialized = True
