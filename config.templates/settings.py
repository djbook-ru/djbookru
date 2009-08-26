# -*- coding: utf-8 -*-

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEFAULT_CHARSET = 'UTF-8'

ADMINS = (
    ('Ruslan Popov', 'ruslan.popov@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'djbookru'
DATABASE_USER = 'djbookru'
DATABASE_PASSWORD = 'topsecret'
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
USE_I18N = True

SITE_ID = 1


MEDIA_ROOT = '/home/rad/django/djbookru/media/'
MEDIA_URL = 'http://djbookru/media/'
ADMIN_MEDIA_PREFIX = 'http://djbookru/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'topsecret'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'urls'

current_dir = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(current_dir, 'templates'),
    '/home/rad/django.apps/djbookru/templates',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.webdesign',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

FILES = '/home/rad/django.apps/djbookru/files'
DJANGOBOOK_PAGE_ZIP = {'1': '%s/djangobook.html.v1.zip' % FILES,
                       '2': '%s/djangobook.html.v2.zip' % FILES}

