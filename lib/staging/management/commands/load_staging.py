from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models.loading import get_apps
from optparse import make_option
from staging.signals import on_load_staging
import os
import re


class Command(BaseCommand):
    requires_model_validation = True
    help = (u'Load all fixtures with staging_ prefix. '
        u'If env is defined: fixtures with {{ env }}_staging_ will be loaded and the end, '
        u'so you can overwride some data.')

    option_list = BaseCommand.option_list + (
        make_option('--env', '-e', dest='env',
            help='enviroment'),
    )

    def handle(self, *args, **kwargs):
        if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
            if raw_input('Database engine is not SQLite. Do you wish load staging data? [y/N]') != 'y':
                return

        env = kwargs.get('env')
        options = kwargs.get('options', {})

        app_module_paths = []
        for app in get_apps():
            if hasattr(app, '__path__'):
                # It's a 'models/' subpackage
                for path in app.__path__:
                    app_module_paths.append(path)
            else:
                # It's a models.py module
                app_module_paths.append(app.__file__)

        app_fixtures = [os.path.join(os.path.dirname(path), 'fixtures') for path in app_module_paths]
        app_fixtures += settings.FIXTURE_DIRS

        fixtures = []

        for app in app_fixtures:
            if os.path.exists(app):
                fixtures.extend(self.load_path(app, options, env))

        call_command('loaddata', *fixtures, **options)

        on_load_staging.send(app_fixtures)

    def load_path(self, path, options, env):
        fixture_pattern = re.compile(r'^staging_.+\.(json|yaml|xml)$')
        fixtures = sorted([i for i in os.listdir(path) if fixture_pattern.match(i)])

        if env:
            fixture_pattern = re.compile(r'^%s_staging_.+\.(json|yaml|xml)$' % env)
            fixtures.extend(sorted([i for i in os.listdir(path) if fixture_pattern.match(i)]))

        return fixtures
