# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oembed.providers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregateMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('object_id', models.IntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(related_name='aggregate_media', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoredOEmbed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match', models.TextField()),
                ('response_json', models.TextField()),
                ('resource_type', models.CharField(max_length=8, editable=False, choices=[(b'photo', b'Photo'), (b'video', b'Video'), (b'rich', b'Rich'), (b'link', b'Link')])),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_expires', models.DateTimeField(null=True, blank=True)),
                ('maxwidth', models.IntegerField(null=True, blank=True)),
                ('maxheight', models.IntegerField(null=True, blank=True)),
                ('object_id', models.IntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(related_name='related_storedoembed', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('-date_added',),
                'verbose_name': 'stored OEmbed',
                'verbose_name_plural': 'stored OEmbeds',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoredProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('endpoint_url', models.CharField(max_length=255)),
                ('regex', models.CharField(max_length=255)),
                ('wildcard_regex', models.CharField(help_text=b'Wild-card version of regex', max_length=255, blank=True)),
                ('resource_type', models.CharField(max_length=8, choices=[(b'photo', b'Photo'), (b'video', b'Video'), (b'rich', b'Rich'), (b'link', b'Link')])),
                ('active', models.BooleanField(default=False)),
                ('provides', models.BooleanField(default=False, help_text=b'Provide upstream')),
                ('scheme_url', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'ordering': ('endpoint_url', 'resource_type', 'wildcard_regex'),
            },
            bases=(models.Model, oembed.providers.HTTPProvider),
        ),
    ]
