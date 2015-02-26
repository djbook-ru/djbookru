# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('content', models.TextField(max_length=1000, verbose_name='comment')),
                ('submit_date', models.DateTimeField(auto_now_add=True, verbose_name='submit date')),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_comment', to='contenttypes.ContentType')),
                ('reply_to', models.ForeignKey(verbose_name='reply to', blank=True, to='comments.Comment', null=True)),
                ('user', models.ForeignKey(verbose_name='user', to='accounts.User')),
            ],
            options={
                'ordering': ('submit_date',),
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
    ]
