# -*- coding: utf-8 -*-

import os
import tempfile
from functools import wraps
from datetime import datetime

from fabric.api import local, run, env, get

__all__ = ('make_instance', 'drop_instance', 'db_dump',)


MYSQLDUMP_CMD_TPL = """
mysqldump -h %(db_host)s -u %(user_name)s -p%(password)s %(db_name)s > %(filename)s
"""
MYSQL_CMD_TPL = """mysql -h %(db_host)s -P %(db_port)s -u root -p%(root)s < %(filename)s"""
DB_CREATE_TPL = """create database if not exists `%(db_name)s`;"""
DB_DROP_TPL = """drop database if exists `%(db_name)s`;"""
USER_CREATE_TPL = """create user `%(user_name)s`@`%(user_host)s` identified by '%(password)s';"""
USER_DROP_TPL = """drop user `%(user_name)s`@`%(user_host)s`;"""
GRANT_TPL = """grant all on `%(db_name)s`.* to `%(user_name)s`@`%(user_host)s`;"""
REVOKE_TPL = """revoke all privileges on `%(db_name)s`.* from `%(user_name)s`@`%(user_host)s`;"""


def run_sql(func):
    @wraps(func)
    def inner(*args, **kwargs):
        descriptor, filename = tempfile.mkstemp()
        command = func(*args, **kwargs)
        print 'SQL >>> %s' % command
        try:
            os.write(descriptor, command)
        finally:
            os.close(descriptor)

        root_pass = os.environ.get('MYSQL_ROOT_PASSWORD')
        db_host = os.environ.get('MYSQL_HOST', 'localhost')
        db_port = os.environ.get('MYSQL_PORT', 3306)

        local(MYSQL_CMD_TPL % dict(
            root=root_pass,
            db_host=db_host,
            db_port=db_port,
            filename=filename))
        local('rm %s' % filename)
    return inner


@run_sql
def db_create(db_name):
    return DB_CREATE_TPL % dict(db_name=db_name)


@run_sql
def db_drop(db_name):
    return DB_DROP_TPL % dict(db_name=db_name)


@run_sql
def user_create(user_name, password, user_host='localhost'):
    return USER_CREATE_TPL % locals()


@run_sql
def user_drop(user_name, user_host='localhost'):
    return USER_DROP_TPL % locals()


@run_sql
def grant_on(db_name, user_name, user_host='localhost'):
    return GRANT_TPL % locals()


@run_sql
def revoke_from(db_name, user_name, user_host='localhost'):
    return REVOKE_TPL % locals()


def make_instance(db_name, user_name, password, user_host='localhost'):
    u"""Создаёт локальный инстанс БД (имя, юзер, пароль)."""
    db_create(db_name)
    db_create('%s_test' % db_name)
    user_create(user_name, password, user_host)
    grant_on(db_name, user_name, user_host)
    grant_on('%s_test' % db_name, user_name, user_host)


def drop_instance(db_name, user_name, password, user_host='localhost'):
    u"""Удаляет локальный инстанс БД (имя, юзер, пароль)."""
    revoke_from(db_name, user_name, user_host)
    revoke_from('%s_test' % db_name, user_name, user_host)
    user_drop(user_name, user_host)
    db_drop('%s_test' % db_name)
    db_drop(db_name)


def db_dump(**kwargs):
    u"""Создаёт на сервере дамп текущей БД, может скачивать его и удалять."""
    filename = kwargs.get(
        'filename',
        os.path.join(
            env.conf.PROJECT_DIR,
            'dumps',
            '%s.sql' % datetime.now().strftime('%Y%m%d-%H%M%S')))
    run(MYSQLDUMP_CMD_TPL % {
        'db_host': env.conf.DB_HOST,
        'db_name': env.conf.DB_NAME,
        'user_name': env.conf.DB_USER,
        'password': env.conf.DB_PASS,
        'filename': filename
        }, shell=False)
    if 'download' in kwargs:
        get(filename, os.path.basename(filename))
    if 'remove' in kwargs:
        run('rm %s' % filename)
