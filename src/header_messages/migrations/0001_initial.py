# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HeaderMessage'
        db.create_table('header_messages_headermessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=2048)),
        ))
        db.send_create_signal('header_messages', ['HeaderMessage'])


    def backwards(self, orm):
        # Deleting model 'HeaderMessage'
        db.delete_table('header_messages_headermessage')


    models = {
        'header_messages.headermessage': {
            'Meta': {'object_name': 'HeaderMessage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['header_messages']