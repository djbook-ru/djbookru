# -*- coding: utf-8 -*-

from fabric.api import env
from fab_deploy import *
from src import local_settings as settings


@define_host(settings.SERVER_URL)
def production():
    env.shell = settings.SHELL
    return dict(
        WSGI=settings.PROD_WSGI,
        HOST_USER=settings.PROD_HOST_USER,
        HOST_NAME=settings.PROD_HOST_NAME,
        ENV_DIR=settings.PROD_ENV_DIR,
        PROJECT_DIR=settings.PROD_HOST_DIR,
        PIP_REQS_PATH=settings.PIP_REQS_PATH,
        PIP_REQS_BASE=settings.PIP_REQS_BASE,
        DB_HOST=settings.PROD_DB_HOST,
        DB_NAME=settings.PROD_DB_NAME,
        DB_USER=settings.PROD_DB_USER,
        DB_PASS=settings.PROD_DB_PASS,
        #MIGRATE_DUMP=settings.PRE_MIGRATE_DUMP,
        CONFIG='prod_settings.py',
    )
