# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.UsefulLink(url=u'http://groups.google.ru/group/django-russian', name=u'Русская группа на Google', order=1).save()
        orm.UsefulLink(url=u'https://www.djangopackages.com/', name=u'Django Packages', order=2).save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'links.usefullink': {
            'Meta': {'object_name': 'UsefulLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['links']
    symmetrical = True
