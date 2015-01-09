# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'archive link',
                'verbose_name_plural': 'archive links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'source code',
                'verbose_name_plural': 'source codes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsefulLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'useful link',
                'verbose_name_plural': 'useful links',
            },
            bases=(models.Model,),
        ),
    ]
