# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.utils.html import strip_tags, linebreaks
from django.db.utils import DatabaseError


class Migration(DataMigration):

    def forwards(self, orm):
        if db.dry_run:
            return

        print '>>> Migrate dinette.SuperCategory...'

        try:
            for sc in orm['dinette.SuperCategory'].objects.all():
                new_sc = orm.Category()
                new_sc.pk = sc.pk
                new_sc.name = sc.name
                new_sc.position = sc.ordering
                new_sc.save()

            print '>>> Migrate dinette.Category'

            for category in orm['dinette.Category'].objects.all():
                new_forum = orm.Forum()
                new_forum.pk = category.pk
                new_forum.category_id = category.super_category_id
                new_forum.name = category.name
                new_forum.position = category.ordering
                new_forum.description = category.description
                new_forum.save()
                new_forum.moderators = category.moderated_by.all()

            print '>>> Migrate dinette.Ftopics'

            for topic in orm['dinette.Ftopics'].objects.all():
                new_topic = orm.Topic()
                new_topic.pk = topic.pk
                new_topic.forum_id = topic.category_id
                new_topic.user = topic.posted_by
                new_topic.name = topic.subject
                new_topic.views = topic.viewcount
                new_topic.sticky = topic.is_sticky
                new_topic.closed = topic.is_closed
                new_topic.created = topic.created_on
                new_topic.updated = topic.updated_on
                new_topic.save()

                topic_post = orm.Post()
                topic_post.topic = new_topic
                topic_post.user = new_topic.user
                topic_post.body = topic.message
                topic_post.body_html = linebreaks(strip_tags(topic.message))
                topic_post.save()

                topic_post.topic.forum.last_post = topic_post
                topic_post.topic.forum.save()
                topic_post.topic.last_post = topic_post
                topic_post.topic.save()

            print '>>> Migrate dinette.Reply'

            for reply in orm['dinette.Reply'].objects.order_by('created_on'):
                new_post = orm.Post()
                new_post.topic_id = reply.topic_id
                new_post.user = reply.posted_by
                new_post.body = reply.message
                new_post.body_html = linebreaks(strip_tags(reply.message))
                new_post.created = reply.created_on
                new_post.updated = reply.updated_on
                new_post.save()

                new_post.topic.forum.last_post = new_post
                new_post.topic.forum.save()
                new_post.topic.last_post = new_post
                new_post.topic.save()

            print '>>> Fix Forum.post_count and Forum.topic_count'

            for forum in orm.Forum.objects.all():
                forum.post_count = orm.Post.objects.filter(topic__forum=forum).count()
                forum.topic_count = forum.topics.count()
                forum.save()

            print '>>> Fix Topic.post_count'

            for topic in orm.Topic.objects.all():
                topic.post_count = topic.posts.count()
                topic.save()
        except DatabaseError:
            pass

    def backwards(self, orm):
        "Write your backwards methods here."


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
        'dinette.category': {
            'Meta': {'ordering': "('ordering', '-created_on')", 'object_name': 'Category'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderated_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moderaters'", 'symmetrical': 'False', 'to': "orm['accounts.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cposted'", 'to': "orm['accounts.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '110', 'db_index': 'True'}),
            'super_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dinette.SuperCategory']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'dinette.ftopics': {
            'Meta': {'ordering': "('-is_sticky', '-last_reply_on')", 'object_name': 'Ftopics'},
            'announcement_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attachment_type': ('django.db.models.fields.CharField', [], {'default': "'nofile'", 'max_length': '20'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dinette.Category']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "'dummyname.txt'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_reply_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'num_replies': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'replies': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '999'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'viewcount': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'dinette.navlink': {
            'Meta': {'object_name': 'NavLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'dinette.reply': {
            'Meta': {'ordering': "('created_on',)", 'object_name': 'Reply'},
            'attachment_type': ('django.db.models.fields.CharField', [], {'default': "'nofile'", 'max_length': '20'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "'dummyname.txt'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'reply_number': ('django.db.models.fields.SmallIntegerField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dinette.Ftopics']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'dinette.siteconfig': {
            'Meta': {'object_name': 'SiteConfig'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tag_line': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'dinette.supercategory': {
            'Meta': {'ordering': "('-ordering', 'created_on')", 'object_name': 'SuperCategory'},
            'accessgroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'can_access_forums'", 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'djangobb_forum.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['djangobb_forum.Post']"}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        'djangobb_forum.ban': {
            'Meta': {'object_name': 'Ban'},
            'ban_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ban_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ban_users'", 'unique': 'True', 'to': "orm['accounts.User']"})
        },
        'djangobb_forum.category': {
            'Meta': {'ordering': "['position']", 'object_name': 'Category'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'djangobb_forum.forum': {
            'Meta': {'ordering': "['position']", 'object_name': 'Forum'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forums'", 'to': "orm['djangobb_forum.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'last_forum_post'", 'null': 'True', 'to': "orm['djangobb_forum.Post']"}),
            'moderators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['accounts.User']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'topic_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'djangobb_forum.post': {
            'Meta': {'ordering': "['created']", 'object_name': 'Post'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.CharField', [], {'default': "'bbcode'", 'max_length': '15'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['djangobb_forum.Topic']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['accounts.User']"}),
            'user_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'djangobb_forum.posttracking': {
            'Meta': {'object_name': 'PostTracking'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_read': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'topics': ('src.djangobb_forum.fields.JSONField', [], {'null': 'True'}),
            'user': ('src.djangobb_forum.fields.AutoOneToOneField', [], {'to': "orm['accounts.User']", 'unique': 'True'})
        },
        'djangobb_forum.profile': {
            'Meta': {'object_name': 'Profile'},
            'aim': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'icq': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'markup': ('django.db.models.fields.CharField', [], {'default': "'bbcode'", 'max_length': '15'}),
            'msn': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'privacy_permission': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'show_avatar': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_signatures': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_smilies': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '80'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '3.0'}),
            'user': ('src.djangobb_forum.fields.AutoOneToOneField', [], {'related_name': "'forum_profile'", 'unique': 'True', 'to': "orm['accounts.User']"}),
            'yahoo': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        'djangobb_forum.report': {
            'Meta': {'object_name': 'Report'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangobb_forum.Post']"}),
            'reason': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': "'1000'", 'blank': 'True'}),
            'reported_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reported_by'", 'to': "orm['accounts.User']"}),
            'zapped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zapped_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'zapped_by'", 'null': 'True', 'to': "orm['accounts.User']"})
        },
        'djangobb_forum.reputation': {
            'Meta': {'unique_together': "(('from_user', 'post'),)", 'object_name': 'Reputation'},
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reputations_from'", 'to': "orm['accounts.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post'", 'to': "orm['djangobb_forum.Post']"}),
            'reason': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'sign': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reputations_to'", 'to': "orm['accounts.User']"})
        },
        'djangobb_forum.topic': {
            'Meta': {'ordering': "['-updated']", 'object_name': 'Topic'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': "orm['djangobb_forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'last_topic_post'", 'null': 'True', 'to': "orm['djangobb_forum.Post']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'subscriptions'", 'blank': 'True', 'to': "orm['accounts.User']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['dinette', 'djangobb_forum']
