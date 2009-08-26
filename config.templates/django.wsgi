# -*- coding: utf-8 -*-

import os, sys

sys.stdout = sys.stderr # для записи в журнал apache

sys.path.insert(0, os.path.dirname(__file__))
sys.path.append('/home/rad/django.engine')
sys.path.append('/home/rad/django.apps')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
