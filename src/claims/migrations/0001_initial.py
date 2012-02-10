# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Claims'
        db.create_table('claims_claims', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ctx_left', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('selected', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ctx_right', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('claims', ['Claims'])

        # Adding model 'ClaimStatus'
        db.create_table('claims_claimstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('claim', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['claims.Claims'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('applied', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('claims', ['ClaimStatus'])

        # Adding model 'Text'
        db.create_table('claims_text', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('claims', ['Text'])


    def backwards(self, orm):
        
        # Deleting model 'Claims'
        db.delete_table('claims_claims')

        # Deleting model 'ClaimStatus'
        db.delete_table('claims_claimstatus')

        # Deleting model 'Text'
        db.delete_table('claims_text')


    models = {
        'claims.claims': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'Claims'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'ctx_left': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ctx_right': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'selected': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
