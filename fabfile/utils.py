# -*- coding: utf-8 -*-

from functools import wraps
from fabric.api import env, run, cd, prefix


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


@inside_project
def manage(command):
    run('python manage.pyc ' + command, shell=False)
