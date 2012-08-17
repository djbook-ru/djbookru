# -*- coding: utf-8 -*-

from fab_deploy import *
from src import local_settings as settings

COMMON_OPTIONS = dict(
    ENV_DIR=settings.ENV_DIR,
    PROJECT_DIR=settings.PROJECT_DIR,
    DB_HOST=settings.DB_HOST,
    DB_NAME=settings.DB_NAME,
    DB_USER=settings.DB_USER,
    DB_PASS=settings.DB_PASS,
    MIGRATE_DUMP=settings.PRE_MIGRATE_DUMP,
    )


@define_host(settings.SERVER_URL)
def production():
    options = COMMON_OPTIONS.copy()
    return options
