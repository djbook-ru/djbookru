# -*- coding: utf-8 -*-

import os
import sys
from subprocess import Popen, PIPE, STDOUT

from fabric.api import cd, env, local, run, put
from fabric.contrib.project import rsync_project

from database import make_instance, drop_instance, db_dump
from pip import pip_install
from utils import manage, touch, remove_pycs_local, remove_pycs_remote

import src.local_settings as settings

def deploy_server(**kwargs):
    u"""Основная команда для выкладывания кода на сервер."""
    # Компилируем переводы, если это требуется
    if 'po' in kwargs:
        local('./po_compile.sh')
    # Передаём код на сервер
    if 'rsync' in kwargs:
        target = '%(user)s@%(host)s:%(dir)s' % {
            'user': env.conf.HOST_USER,
            'host': env.conf.HOST_NAME,
            'dir': env.conf.PROJECT_DIR,
        }
        print 'Rsync project with %s' % target
        local('rsync -v --stats --archive --recursive --update %(exclude)s %(src)s %(target)s' % {
                'exclude': ' '.join(
                    map(
                        lambda x: '--exclude "%s"' % x,
                        ['.git/', '.gitignore', '*.sql', '*.sql.bz2', '*.sh', '*.rst', '*.po',
                         '*.pyc', '*.sqlite', '*template',
                         'cache/', 'env/', 'fabfile/', 'dumps/', 'logs/', 'sshfs/', 'tmp/',
                         'src/public/', 'src/search',
                         'wsgi.py', 'settings_dump.py', 'test_settings.py',
                         'local_settings.py', 'prod_settings.py'
                         ])),
                'src': '.',
                'target': target
            })
        put('./src/%s' % env.conf.CONFIG, os.path.join(env.conf.PROJECT_DIR, 'src', 'local_settings.py'))
    # Установка/обновление зависимостей
    if 'pip' in kwargs:
        options = ''
        if 'u' == kwargs.get('pip', 'i').lower():
            options = '-U'
        pip_install(options=options)
    # Накат миграций, если это требуется
    if 'migrate' in kwargs:
        db_dump()
        manage('syncdb --migrate --noinput')

    if 'static' in kwargs:
        manage('collectstatic --noinput')
    if 'i18n' in kwargs:
        manage('update_translation_fields')
    if 'haystack' in kwargs:
        manage('rebuild_index --noinput')
    if 'touch' in kwargs:
        touch()


def importing(**kwargs):
    u"""Импорт данных с сервера."""
    # Получаем пользовательскую статику с сервера
    if 'rsync' not in kwargs and 'database' not in kwargs:
        print 'Usage: importing:[rsync=y][,database=y]'
        return
    if 'rsync' in kwargs:
        resource = '%(user)s@%(host)s:%(dir)s' % {
            'user': env.conf.HOST_USER,
            'host': env.conf.HOST_NAME,
            'dir': env.conf.PROJECT_DIR,
        }
        print 'Rsync project with %s' % resource
        local('rsync -v --stats --archive --delete %(src)s %(target)s' % {
                'src': '%s/src/public/media' % resource,
                'target': './src/public/'
            })
    # Получение дампа БД
    if 'database' in kwargs:
        db_dump(filename='import.sql', download=True, remove=True)
        p = Popen(['python', 'manage.py', 'dbshell'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout_data = p.communicate(input='\. import.sql')[0]
        print stdout_data


from . hosts import production

production()
