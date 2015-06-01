#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings


TOPICS_ON_PAGE = getattr(settings, 'FORUM_TOPICS_ON_PAGE', 20)
POSTS_ON_PAGE = getattr(settings, 'FORUM_POSTS_ON_PAGE', 50)
FORUM_EDIT_TIMEOUT = getattr(settings, 'FORUM_EDIT_TIMEOUT', 60)
