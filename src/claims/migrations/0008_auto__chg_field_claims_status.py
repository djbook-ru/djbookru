# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Claims.status'
        db.alter_column('claims_claims', 'status', self.gf('django.db.models.fields.IntegerField')(max_length=1))


    def backwards(self, orm):
        
        # Changing field 'Claims.status'
        db.alter_column('claims_claims', 'status', self.gf('django.db.models.fields.CharField')(max_length=1))


    models = {
        'claims.claims': {
            'Meta': {'ordering': "('reg_datetime',)", 'object_name': 'Claims'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'ctx_left': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ctx_right': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reg_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'reply': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'selected': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'status_applied': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['claims']
