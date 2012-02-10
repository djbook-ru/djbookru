# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PollType'
        db.create_table('poll_polltype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('index', self.gf('django.db.models.fields.SmallIntegerField')(unique=True)),
        ))
        db.send_create_signal('poll', ['PollType'])

        # Adding model 'Poll'
        db.create_table('poll_poll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('queue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Queue'], null=True, blank=True)),
            ('polltype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.PollType'])),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('poll', ['Poll'])

        # Adding M2M table for field votes on 'Poll'
        db.create_table('poll_poll_votes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm['poll.poll'], null=False)),
            ('vote', models.ForeignKey(orm['poll.vote'], null=False))
        ))
        db.create_unique('poll_poll_votes', ['poll_id', 'vote_id'])

        # Adding model 'Queue'
        db.create_table('poll_queue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('auth', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('poll', ['Queue'])

        # Adding model 'Item'
        db.create_table('poll_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Poll'])),
            ('userbox', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('index', self.gf('django.db.models.fields.SmallIntegerField')(default='0')),
        ))
        db.send_create_signal('poll', ['Item'])

        # Adding model 'Vote'
        db.create_table('poll_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Poll'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('poll', ['Vote'])

        # Adding model 'Choice'
        db.create_table('poll_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Vote'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Item'])),
            ('uservalue', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('poll', ['Choice'])


    def backwards(self, orm):
        
        # Deleting model 'PollType'
        db.delete_table('poll_polltype')

        # Deleting model 'Poll'
        db.delete_table('poll_poll')

        # Removing M2M table for field votes on 'Poll'
        db.delete_table('poll_poll_votes')

        # Deleting model 'Queue'
        db.delete_table('poll_queue')

        # Deleting model 'Item'
        db.delete_table('poll_item')

        # Deleting model 'Vote'
        db.delete_table('poll_vote')

        # Deleting model 'Choice'
        db.delete_table('poll_choice')


    models = {
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
        'poll.choice': {
            'Meta': {'object_name': 'Choice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Item']"}),
            'uservalue': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Vote']"})
        },
        'poll.item': {
            'Meta': {'ordering': "['index']", 'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.SmallIntegerField', [], {'default': "'0'"}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Poll']"}),
            'userbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'poll.poll': {
            'Meta': {'ordering': "['-startdate']", 'object_name': 'Poll'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polltype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.PollType']"}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'queue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Queue']", 'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'votes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'poll_poll_related'", 'blank': 'True', 'to': "orm['poll.Vote']"})
        },
        'poll.polltype': {
            'Meta': {'ordering': "['-index']", 'object_name': 'PollType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.SmallIntegerField', [], {'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'poll.queue': {
            'Meta': {'ordering': "['-title']", 'object_name': 'Queue'},
            'auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'poll.vote': {
            'Meta': {'object_name': 'Vote'},
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['poll.Item']", 'through': "orm['poll.Choice']", 'symmetrical': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Poll']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['poll']
