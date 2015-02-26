# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='content')),
                ('page', models.CharField(max_length=500, verbose_name='path to page')),
                ('page_title', models.CharField(max_length=500, verbose_name='page title')),
                ('xpath', models.CharField(max_length=500, verbose_name='xpath')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(0, 'none'), (1, 'accepted'), (2, 'closed')])),
                ('author', models.ForeignKey(related_name='doc_comments', verbose_name='author', to='accounts.User')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'doc. comment',
                'verbose_name_plural': 'doc. comments',
            },
            bases=(models.Model,),
        ),
    ]
