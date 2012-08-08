# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Video.description'
        db.add_column('videos_video', 'description', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Video.description'
        db.delete_column('videos_video', 'description')


    models = {
        'videos.video': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Video'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'video': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['videos']
