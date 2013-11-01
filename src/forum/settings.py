#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


POSTS_ON_PAGE = getattr(settings, 'FORUM_POSTS_ON_PAGE', 100)
FORUM_EDIT_TIMEOUT = getattr(settings, 'FORUM_EDIT_TIMEOUT', 15)
