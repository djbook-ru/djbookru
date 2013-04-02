# -*- coding: utf-8 -*-

import simplejson
from datetime import timedelta

from django.utils import timezone

from admin_tools.utils import AppListElementMixin
from admin_tools.dashboard.modules import DashboardModule

from . import models


class AdClickReport(DashboardModule, AppListElementMixin):
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
        super(AdClickReport, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        if self._initialized:
            return

        end = timezone.now().date()
        start = end - timedelta(days=30)

        self.children = simplejson.dumps(models.AdClick.by_period(start, end))
        self._initialized = True
