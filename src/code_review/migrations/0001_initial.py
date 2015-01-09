# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging_autocomplete.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('row', models.PositiveIntegerField(verbose_name='row')),
                ('content', models.TextField(max_length=1000, verbose_name='comment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('author', models.ForeignKey(related_name='code_comments', verbose_name='author', to='accounts.User')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000, verbose_name='file name')),
                ('content', models.TextField(verbose_name='content')),
                ('language', models.CharField(blank=True, max_length=100, verbose_name='language', choices=[(b'python', 'Python'), (b'javascript', 'JavaScript'), (b'bash', 'Bash'), (b'sql', 'SQL'), (b'xml', 'XML/HTML')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Snipet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('language', models.CharField(default=b'python', help_text='Main snippet language', max_length=100, verbose_name='language', choices=[(b'python', 'Python'), (b'javascript', 'JavaScript')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('tags', tagging_autocomplete.models.TagAutocompleteField(max_length=255, verbose_name='tags', blank=True)),
                ('rating', models.PositiveIntegerField(default=0, verbose_name='rating')),
                ('author', models.ForeignKey(verbose_name='author', to='accounts.User')),
                ('rated_by', models.ManyToManyField(verbose_name='rated by', editable=False, to='accounts.User', related_name='rated_snippets')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='file',
            name='snipet',
            field=models.ForeignKey(to='code_review.Snipet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='file',
            field=models.ForeignKey(verbose_name='file', to='code_review.File'),
            preserve_default=True,
        ),
    ]
