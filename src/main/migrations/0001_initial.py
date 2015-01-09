# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('toc', models.TextField(verbose_name='ToC', blank=True)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.CharField(max_length=100, verbose_name='slug')),
                ('content', models.TextField(verbose_name='content')),
                ('chapter', models.CharField(max_length=10, verbose_name='chapter', blank=True)),
                ('section', models.CharField(max_length=10, verbose_name='section', blank=True)),
                ('book', models.ForeignKey(related_name='pages', verbose_name='book', to='main.Book')),
            ],
            options={
                'ordering': ['chapter', 'section'],
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('slug', 'book')]),
        ),
    ]
