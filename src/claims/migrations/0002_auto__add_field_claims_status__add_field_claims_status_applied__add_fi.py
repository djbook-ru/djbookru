# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Claims.status'
        db.add_column('claims_claims', 'status', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'Claims.status_applied'
        db.add_column('claims_claims', 'status_applied', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2010, 12, 3), blank=True), keep_default=False)

        # Adding field 'Claims.reply'
        db.add_column('claims_claims', 'reply', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Changing field 'Claims.datetime'
        db.alter_column('claims_claims', 'datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))


    def backwards(self, orm):

        # Deleting field 'Claims.status'
        db.delete_column('claims_claims', 'status')

        # Deleting field 'Claims.status_applied'
        db.delete_column('claims_claims', 'status_applied')

        # Deleting field 'Claims.reply'
        db.delete_column('claims_claims', 'reply')

        # Changing field 'Claims.datetime'
        db.alter_column('claims_claims', 'datetime', self.gf('django.db.models.fields.DateTimeField')())


    models = {
        'claims.claims': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'Claims'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'ctx_left': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ctx_right': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reply': ('django.db.models.fields.TextField', [], {}),
            'selected': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'status_applied': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'claims.claimstatus': {
            'Meta': {'object_name': 'ClaimStatus'},
            'applied': ('django.db.models.fields.DateTimeField', [], {}),
            'claim': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['claims.Claims']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'claims.text': {
            'Meta': {'object_name': 'Text'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['claims']
