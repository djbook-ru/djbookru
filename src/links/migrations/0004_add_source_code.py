# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.SourceCode(url=u'https://github.com/Alerion/django_documentation/https://github.com/Alerion/django_documentation/',
            name=u'Перевод документации', order=1).save()
        orm.SourceCode(url=u'https://github.com/RaD/djbookru/', name=u'Наш сайт', order=2).save()
        orm.SourceCode(url=u'https://github.com/django/', name=u'Django', order=3).save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'links.sourcecode': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SourceCode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'links.usefullink': {
            'Meta': {'ordering': "('order',)", 'object_name': 'UsefulLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['links']
    symmetrical = True
