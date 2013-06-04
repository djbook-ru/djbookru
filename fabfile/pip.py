# -*- coding: utf-8 -*-

import os
from fabric.api import env, run

from . utils import pip_reqs_path, inside_project, inside_virtualenv


@inside_virtualenv
@inside_project
def pip_install(what=None, options='', restart=True):
    what = pip_reqs_path(what or env.conf.PIP_REQS_BASE)
    run('pip install %s -r %s' % (options, what))
