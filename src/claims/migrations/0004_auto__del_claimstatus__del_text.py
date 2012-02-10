# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ClaimStatus'
        db.delete_table('claims_claimstatus')

        # Deleting model 'Text'
        db.delete_table('claims_text')


    def backwards(self, orm):
        
        # Adding model 'ClaimStatus'
        db.create_table('claims_claimstatus', (
            ('applied', self.gf('django.db.models.fields.DateTimeField')()),
            ('claim', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['claims.Claims'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('claims', ['ClaimStatus'])

        # Adding model 'Text'
        db.create_table('claims_text', (
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('claims', ['Text'])


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
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'status_applied': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['claims']
