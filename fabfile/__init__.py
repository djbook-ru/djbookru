# -*- coding: utf-8 -*-

from fabric import api

from . import utils


@utils.inside_virtualenv
def deploy_server(migrate=False, static=False, i18n=False, haystack=False, touch=True):
    tpl = 'mysqldump -h %(host)s -u %(user)s -p%(passwd)s %(name)s > %(migrate)s'
    if migrate:
        context = dict(
            host=api.env.conf.DB_HOST,
            name=api.env.conf.DB_NAME,
            user=api.env.conf.DB_USER,
            passwd=api.env.conf.DB_PASS,
            migrate=api.env.conf.MIGRATE_DUMP,
            )
        api.run(tpl % context, shell=False)
        utils.manage('syncdb --migrate --noinput')
    if static:
        utils.manage('collectstatic --noinput')
    if i18n:
        utils.manage('update_translation_fields')
    if haystack:
        utils.manage('rebuild_index --noinput')
    if touch:
        api.run('touch ~/www/site1/webapp/webapp.wsgi', shell=False)


from . hosts import production

production()
