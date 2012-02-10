# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Language'
        db.create_table('docbook_translator_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('original_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('docbook_translator', ['Language'])

        # Adding model 'Book'
        db.create_table('docbook_translator_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('original_description', self.gf('django.db.models.fields.TextField')()),
            ('original_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docbook_translator.Language'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translated_books', to=orm['docbook_translator.Language'])),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('docbook_translator', ['Book'])

        # Adding M2M table for field moderators on 'Book'
        db.create_table('docbook_translator_book_moderators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['docbook_translator.book'], null=False)),
            ('user', models.ForeignKey(orm['accounts.user'], null=False))
        ))
        db.create_unique('docbook_translator_book_moderators', ['book_id', 'user_id'])

        # Adding M2M table for field translators on 'Book'
        db.create_table('docbook_translator_book_translators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['docbook_translator.book'], null=False)),
            ('user', models.ForeignKey(orm['accounts.user'], null=False))
        ))
        db.create_unique('docbook_translator_book_translators', ['book_id', 'user_id'])

        # Adding model 'Chapter'
        db.create_table('docbook_translator_chapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docbook_translator.Book'])),
            ('original_name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('original_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('original_text', self.gf('django.db.models.fields.TextField')()),
            ('namber', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('docbook_translator', ['Chapter'])

        # Adding model 'TextNode'
        db.create_table('docbook_translator_textnode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docbook_translator.Chapter'])),
            ('original_text', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('docbook_translator', ['TextNode'])

        # Adding model 'TextNodeVersion'
        db.create_table('docbook_translator_textnodeversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text_node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docbook_translator.TextNode'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('moderator_rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('docbook_translator', ['TextNodeVersion'])

        # Adding unique constraint on 'TextNodeVersion', fields ['text_node', 'approved']
        db.create_unique('docbook_translator_textnodeversion', ['text_node_id', 'approved'])

        # Adding model 'Comment'
        db.create_table('docbook_translator_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text_node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['docbook_translator.TextNode'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translator_comments', to=orm['accounts.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('docbook_translator', ['Comment'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TextNodeVersion', fields ['text_node', 'approved']
        db.delete_unique('docbook_translator_textnodeversion', ['text_node_id', 'approved'])

        # Deleting model 'Language'
        db.delete_table('docbook_translator_language')

        # Deleting model 'Book'
        db.delete_table('docbook_translator_book')

        # Removing M2M table for field moderators on 'Book'
        db.delete_table('docbook_translator_book_moderators')

        # Removing M2M table for field translators on 'Book'
        db.delete_table('docbook_translator_book_translators')

        # Deleting model 'Chapter'
        db.delete_table('docbook_translator_chapter')

        # Deleting model 'TextNode'
        db.delete_table('docbook_translator_textnode')

        # Deleting model 'TextNodeVersion'
        db.delete_table('docbook_translator_textnodeversion')

        # Deleting model 'Comment'
        db.delete_table('docbook_translator_comment')


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User', '_ormbases': ['auth.User']},
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'docbook_translator.book': {
            'Meta': {'object_name': 'Book'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translated_books'", 'to': "orm['docbook_translator.Language']"}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'moderators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'moderated_books'", 'blank': 'True', 'to': "orm['accounts.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'original_description': ('django.db.models.fields.TextField', [], {}),
            'original_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docbook_translator.Language']"}),
            'original_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'translators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'translated_books'", 'blank': 'True', 'to': "orm['accounts.User']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'docbook_translator.chapter': {
            'Meta': {'object_name': 'Chapter'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docbook_translator.Book']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'namber': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'original_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'original_text': ('django.db.models.fields.TextField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'docbook_translator.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translator_comments'", 'to': "orm['accounts.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text_node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docbook_translator.TextNode']"})
        },
        'docbook_translator.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'original_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'docbook_translator.textnode': {
            'Meta': {'object_name': 'TextNode'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docbook_translator.Chapter']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'original_text': ('django.db.models.fields.TextField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'docbook_translator.textnodeversion': {
            'Meta': {'unique_together': "(('text_node', 'approved'),)", 'object_name': 'TextNodeVersion'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator_rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'text_node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['docbook_translator.TextNode']"})
        }
    }

    complete_apps = ['docbook_translator']
