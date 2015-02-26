# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import src.forum.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('position', models.IntegerField(default=0, verbose_name='Position')),
                ('groups', models.ManyToManyField(help_text='Only users from these groups can see this category', related_name='forum_categories', verbose_name='Groups', to='auth.Group', blank=True)),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('position', models.IntegerField(default=0, verbose_name='Position')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('category', models.ForeignKey(related_name='forums', verbose_name='Category', to='forum.Category')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(null=True, verbose_name='Updated', blank=True)),
                ('body', models.TextField(verbose_name='Message')),
                ('rating', models.IntegerField(default=0, verbose_name='rating')),
            ],
            options={
                'ordering': ['created'],
                'get_latest_by': 'created',
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
            bases=(models.Model, src.forum.models.RatingMixin),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='subject')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated')),
                ('views', models.IntegerField(default=0, verbose_name='views count')),
                ('sticky', models.BooleanField(default=False, verbose_name='sticky')),
                ('closed', models.BooleanField(default=False, verbose_name='closed')),
                ('heresy', models.BooleanField(default=False, verbose_name='heresy')),
                ('rating', models.IntegerField(default=0, verbose_name='rating')),
                ('send_response', models.BooleanField(default=False, verbose_name='send response on email')),
                ('forum', models.ForeignKey(related_name='topics', verbose_name='forum', to='forum.Forum')),
                ('user', models.ForeignKey(related_name='forum_topics', verbose_name='user', to='accounts.User')),
            ],
            options={
                'ordering': ['-sticky', '-updated'],
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
            bases=(models.Model, src.forum.models.RatingMixin),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='time')),
                ('topic', models.ForeignKey(verbose_name='topic', to='forum.Topic')),
                ('user', models.ForeignKey(related_name='forum_visits', verbose_name='user', to='accounts.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='visit',
            unique_together=set([('user', 'topic')]),
        ),
        migrations.AddField(
            model_name='topic',
            name='visited_by',
            field=models.ManyToManyField(related_name='visited_topics', verbose_name=b'visited_by', to='accounts.User', through='forum.Visit', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='votes',
            field=models.ManyToManyField(verbose_name='votes', editable=False, to='accounts.User', related_name='voted_topics'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(related_name='posts', verbose_name='Topic', to='forum.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(related_name='forum_updated_posts', verbose_name='Updated by', blank=True, to='accounts.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(related_name='forum_posts', verbose_name='User', to='accounts.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='votes',
            field=models.ManyToManyField(verbose_name='votes', editable=False, to='accounts.User', related_name='voted_posts'),
            preserve_default=True,
        ),
    ]
