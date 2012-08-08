# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from _mysql_exceptions import OperationalError


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting field 'User.last_activity'
        db.delete_column('accounts_user', 'last_activity')

        # Deleting field 'User.last_posttime'
        db.delete_column('accounts_user', 'last_posttime')

        # Deleting field 'User.last_session_activity'
        db.delete_column('accounts_user', 'last_session_activity')

        # Deleting field 'User.signature'
        db.delete_column('accounts_user', 'signature')

        # Deleting field 'User.posts_count'
        db.delete_column('accounts_user', 'posts_count')

    def backwards(self, orm):
        try:
            # Adding field 'User.last_activity'
            db.add_column('accounts_user', 'last_activity', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)
        except OperationalError:
            pass

        try:
            # Adding field 'User.last_posttime'
            db.add_column('accounts_user', 'last_posttime', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)
        except OperationalError:
            pass

        try:
            # Adding field 'User.last_session_activity'
            db.add_column('accounts_user', 'last_session_activity', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)
        except OperationalError:
            pass

        try:
            # Adding field 'User.signature'
            db.add_column('accounts_user', 'signature', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True), keep_default=False)
        except OperationalError:
            pass

        try:
            # Adding field 'User.posts_count'
            db.add_column('accounts_user', 'posts_count', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)
        except OperationalError:
            pass

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
        }
    }

    complete_apps = ['accounts']
