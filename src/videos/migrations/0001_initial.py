# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging_autocomplete.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500, verbose_name='title')),
                ('video', models.URLField(verbose_name='video URL')),
                ('description', models.TextField()),
                ('tags', tagging_autocomplete.models.TagAutocompleteField(max_length=255, verbose_name='tags', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
            },
            bases=(models.Model,),
        ),
    ]
