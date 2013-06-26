# -*- coding: utf-8 -*-

import posixpath

from functools import wraps
from fabric.api import env, run, cd, prefix, local


def virtualenv():
    return prefix('source %s/bin/activate' % env.conf.ENV_DIR)


def inside_virtualenv(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with virtualenv():
            return func(*args, **kwargs)
    return inner


def inside_project(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with cd(env.conf.PROJECT_DIR):
            return func(*args, **kwargs)
    return inner


@inside_virtualenv
@inside_project
def manage(command):
    u"""Выполняет команду Django на сервере."""
    run('python manage.py ' + command, shell=False)


def pip_reqs_path(name):
    if not name.endswith('.txt'):
        name += '.txt'
    return posixpath.join(env.conf.PIP_REQS_PATH, name)


def touch():
    u"""Обновляет время WSGI файла, заставляя сервер перезапустить сайт."""
    run('touch %s' % env.conf.WSGI, shell=False)


def touch_after(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        touch()
        return result
    return inner


def remove_pycs_local():
    u"""Удаление скомпилированных модулей локально."""
    local('find ./src -type f -name "*.pyc" -delete')


def remove_pycs_remote():
    u"""Удаление скомпилированных модулей удалённо."""
    with cd(env.conf.PROJECT_DIR):
        run('find . -type f -name "*.pyc" -delete')
