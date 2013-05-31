# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KVStore'
        db.create_table('thumbnail_kvstore', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True, db_column='key')),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('thumbnail', ['KVStore'])


    def backwards(self, orm):
        # Deleting model 'KVStore'
        db.delete_table('thumbnail_kvstore')


    models = {
        'thumbnail.kvstore': {
            'Meta': {'object_name': 'KVStore'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True', 'db_column': "'key'"}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['thumbnail']