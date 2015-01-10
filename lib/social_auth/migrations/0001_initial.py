# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social_auth.db.base
import social_auth.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_url', models.CharField(max_length=255)),
                ('handle', models.CharField(max_length=255)),
                ('secret', models.CharField(max_length=255)),
                ('issued', models.IntegerField(db_index=True)),
                ('lifetime', models.IntegerField()),
                ('assoc_type', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model, social_auth.db.base.AssociationMixin),
        ),
        migrations.CreateModel(
            name='Nonce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_url', models.CharField(max_length=255)),
                ('timestamp', models.IntegerField(db_index=True)),
                ('salt', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model, social_auth.db.base.NonceMixin),
        ),
        migrations.CreateModel(
            name='UserSocialAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(max_length=32)),
                ('uid', models.CharField(max_length=255)),
                ('extra_data', social_auth.fields.JSONField(default=b'{}')),
                ('user', models.ForeignKey(related_name='social_auth', to='accounts.User')),
            ],
            options={
            },
            bases=(models.Model, social_auth.db.base.UserSocialAuthMixin),
        ),
        migrations.AlterUniqueTogether(
            name='usersocialauth',
            unique_together=set([('provider', 'uid')]),
        ),
        migrations.AlterUniqueTogether(
            name='nonce',
            unique_together=set([('timestamp', 'salt', 'server_url')]),
        ),
    ]
