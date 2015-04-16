# -*- coding: utf-8 -*-

import os
import sys
import glob

gettext_noop = lambda s: s

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rel_project(*x):
    return os.path.abspath(os.path.join(BASE_DIR, *x))

# get local software repositories
# FIXME: Remove lib
sys.path.insert(0, rel_project('lib'))

gettext_noop = lambda s: s

DEBUG = True

SECRET_KEY = 'somedefaultsecretkey'

ALLOWED_HOSTS = ('djbook.ru', 'www.djbook.ru')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'src.forum.middleware.LastLoginMiddleware',
    'src.forum.middleware.UsersOnline',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # FIXME: remove this
    'pagination.middleware.PaginationMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djbookru',
        'USER': 'djbookru',
        'PASSWORD': 'q1',
        'HOST': 'localhost',
        'PORT': '',
    }
}

MIGRATION_MODULES = {
    'auth': 'src.main.migrations_auth',
}

ROOT_URLCONF = 'src.urls'
WSGI_APPLICATION = 'src.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',

    'bootstrapform',
    'pagedown',
    'oembed',
    'pagination',
    'sorl.thumbnail',
    'tagging',
    'ordered_model',
    'social.apps.django_app.default',
    'haystack',
    'haystack_static_pages',

    'src.forum',
    'src.accounts',
    'src.claims',
    'src.comments',
    'src.doc_comments',
    'src.examples',
    'src.main',
    'src.news',
    'src.videos',
    'src.links',
    'src.header_messages',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            rel_project('src/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'social.apps.django_app.context_processors.backends',
                'src.context_processors.custom',
            ],
        },
    },
]

FIXTURE_DIRS = (
    rel_project('src/fixtures'),
)

MEDIA_ROOT = rel_project('src/public/media')
MEDIA_URL = '/media/'
STATIC_ROOT = rel_project('src/public/static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    rel_project('src/static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'support@djbook.ru'

USE_TZ = True
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
LANGUAGES = (
    ('ru', gettext_noop('Russian')),
    ('en', gettext_noop('English')),
)
USE_I18N = True
USE_L10N = False
USE_THOUSAND_SEPARATOR = False
LOCALE_PATHS = (
    rel_project('src/locale'),
    rel_project('src/main/locale'),
)

SITE_ID = 1
SITE_URL = 'http://djbook.ru/'

###########################################################
# AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/auth/login/'
LOGIN_ERROR_URL = LOGIN_URL
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

USER_ONLINE_TIMEOUT = 15
###########################################################

###########################################################
SOCIAL_AUTH_USER_MODEL = 'accounts.User'
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'src.accounts.social_auth_pipelines.check_email',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user'
)

SOCIAL_AUTH_GITHUB_APP_ID = ''
SOCIAL_AUTH_GITHUB_API_SECRET = ''
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_VK_OAUTH2_KEY = ''
SOCIAL_AUTH_VK_OAUTH2_SECRET = ''

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.yandex.YandexOpenId',
    'social.backends.vk.VKOAuth2',
    'src.accounts.backends.CustomUserBackend',
)
###########################################################

###########################################################
DJANGO_DOCUMENTATION_VERSION = '1.8'
DJANGO_DOCUMENTATION_HTML = rel_project('docs/rel%s/' % DJANGO_DOCUMENTATION_VERSION)
DJANGO_DOCUMENTATION_URL = '/rel%s/' % DJANGO_DOCUMENTATION_VERSION
DJANGO_DOCUMENTATION_SITEMAP_URL = '%ssitemap.xml' % DJANGO_DOCUMENTATION_URL
###########################################################

###########################################################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': rel_project('search', 'xapian_index'),
        'HAYSTACK_XAPIAN_LANGUAGE': 'ru',
        # 'INCLUDE_SPELLING': True  # TODO: use this
    },
}


def get_doc_pages():
    for directory, dirnames, filenames in os.walk(DJANGO_DOCUMENTATION_HTML):
        for item in glob.glob('%s/*.html' % directory):
            yield item

HAYSTACK_STATIC_PAGES = tuple(get_doc_pages())
HAYSTACK_STATIC_MAPPING = {
    DJANGO_DOCUMENTATION_HTML: DJANGO_DOCUMENTATION_URL
}
###########################################################

###########################################################
EMAIL_SUBJECT_PREFIX = '[Djbook.ru]'
DATETIME_FORMAT = 'j N Y, G:i'
FEEDBACK_SUBJECT = gettext_noop(u'Feedback message from Djbook.ru')
###########################################################

RECAPTCHA_PUBLIC = ''
RECAPTCHA_PRIVATE = ''

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'plain': {
            'format': '%(asctime)s %(message)s',
        },
        'verbose': {
            'format':
                '%(levelname)s %(asctime)s %(name)s %(process)d %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'main_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': rel_project('logs', 'main.log'),
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'haystack_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': rel_project('logs', 'haystack.log'),
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'profile_db_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': rel_project('logs', 'profile.db.log'),
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'plain',
        }

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'haystack': dict(
            handlers=['haystack_log'],
            level='ERROR',
            propagate=True,
        ),
        'django.db.backends': dict(
            handlers=['profile_db_log'],
            level='ERROR',
            propagate=True,
        )
    }
}

try:
    from local_settings import *
except ImportError:
    pass
