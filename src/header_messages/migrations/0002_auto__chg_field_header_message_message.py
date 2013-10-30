# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Header_message.message'
        db.alter_column('header_messages_header_message', 'message', self.gf('django.db.models.fields.CharField')(max_length=2048))

    def backwards(self, orm):

        # Changing field 'Header_message.message'
        db.alter_column('header_messages_header_message', 'message', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'header_messages.header_message': {
            'Meta': {'ordering': "['-weight']", 'object_name': 'Header_message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['header_messages']