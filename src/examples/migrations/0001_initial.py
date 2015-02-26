# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('content', models.TextField(help_text='Use <a target="blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown</a> and HTML', verbose_name='content')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('approved', models.BooleanField(default=True, help_text='Can be used for draft', verbose_name='approved')),
                ('note', models.TextField(help_text="author's note, is not visible on site", verbose_name='note', blank=True)),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('topic_id', models.IntegerField(default=b'0', verbose_name='Topic ID')),
                ('author', models.ForeignKey(to='accounts.User')),
                ('category', models.ForeignKey(related_name='examples', verbose_name='category', to='examples.Category')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Example',
                'verbose_name_plural': 'Examples',
            },
            bases=(models.Model,),
        ),
    ]
