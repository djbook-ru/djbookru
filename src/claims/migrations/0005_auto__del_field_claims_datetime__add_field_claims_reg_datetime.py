# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Claims.reg_datetime'
        db.add_column('claims_claims', 'reg_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2010, 12, 3), blank=True), keep_default=False)


    def backwards(self, orm):

        # Deleting field 'Claims.reg_datetime'
        db.delete_column('claims_claims', 'reg_datetime')


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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'reply': ('django.db.models.fields.TextField', [], {}),
            'selected': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'status_applied': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['claims']
