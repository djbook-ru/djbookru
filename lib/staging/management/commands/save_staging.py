from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand, CommandError
from django.db.models import FileField, get_app, get_models, get_model
from optparse import make_option
import os
import shutil
import subprocess

STAGING_MEDIA_PATH = getattr(settings, 'STAGING_MEDIA_PATH', 'staging')
STAGING_MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT, STAGING_MEDIA_PATH)


class Command(BaseCommand):
    requires_model_validation = True
    help = (u'This command saves data from DB to staging fixtures. '
            u'Example: \n./manage.py save_staging auth \n'
            u'./manage.py save_staging auth.User\n'
            u'Add --env to save fixtures for some enviroment')

    option_list = BaseCommand.option_list + (
        make_option('--env', '-e', dest='env',
            help='enviroment'),
    )

    def handle(self, *app_labels, **options):
        if not settings.FIXTURE_DIRS:
            raise CommandError('Add fixtures folder for project root to FIXTURE_DIRS for saving apps not from project')

        if options.get('env'):
            env_prefix = options.get('env') + '_'
        else:
            env_prefix = ''

        for app_label in app_labels:
            try:
                app_label, model_label = app_label.split('.')
                models = [get_model(app_label, model_label)]
            except ValueError:
                try:
                    app = get_app(app_label)
                except ImproperlyConfigured, e:
                    raise CommandError(e)
                models = get_models(app)

            fixtures_dir = settings.FIXTURE_DIRS[0]
            if not os.path.exists(fixtures_dir):
                os.makedirs(fixtures_dir)

            for model in models:
                meta = model._meta
                model_name = '%s.%s' % (meta.app_label, meta.object_name)

                fixtures_path = '%s/%sstaging_%s_%s.json' % (fixtures_dir, env_prefix, \
                    meta.app_label.lower(), meta.object_name.lower())
                self.move_files(model)
                print 'saving %s' % model_name
                subprocess.call(['python', 'manage.py', 'dumpdata', model_name, '--indent=2'],
                    stdout=open(fixtures_path, 'w'))

    def move_files(self, model):
        meta = model._meta
        app_label = meta.app_label
        model_name = meta.object_name.lower()

        for field in meta.fields:
            if isinstance(field, FileField) and field in meta.local_fields:
                for obj in model._default_manager.all():
                    file = getattr(obj, field.name)
                    if not file:
                        continue
                    name = file.path.split('/')[-1]
                    dir_path = os.path.join(STAGING_MEDIA_ROOT, app_label, model_name)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    new_path = os.path.abspath(os.path.join(dir_path, name))

                    if file.path != new_path:
                        while os.path.exists(new_path):
                            name = '_' + name
                            new_path = os.path.abspath(os.path.join(dir_path, name))

                        value = new_path[len(os.path.normpath(settings.MEDIA_ROOT)):]
                        if value.startswith('/'):
                            value = value[1:]

                        try:
                            shutil.move(file.path, new_path)
                        except IOError:
                            pass

                        setattr(obj, field.name, value)
                        obj.save()
