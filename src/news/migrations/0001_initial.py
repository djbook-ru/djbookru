# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('content', models.TextField(help_text='Use Markdown and HTML', verbose_name='content')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('approved', models.BooleanField(default=True, help_text='Can be used for draft', verbose_name='approved')),
                ('link', models.CharField(max_length=500, verbose_name='link to original', blank=True)),
                ('author', models.ForeignKey(editable=False, to='accounts.User')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceRSS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('link', models.URLField(verbose_name='link')),
                ('is_active', models.BooleanField(default=True, verbose_name='active?')),
                ('sync_date', models.DateTimeField(verbose_name='last update', null=True, editable=False, blank=True)),
                ('approved_by_default', models.BooleanField(default=False, verbose_name='approved by default?')),
                ('news_author', models.ForeignKey(verbose_name='author', to='accounts.User')),
            ],
            options={
                'verbose_name': 'RSS source',
                'verbose_name_plural': 'RSS sources',
            },
            bases=(models.Model,),
        ),
    ]
