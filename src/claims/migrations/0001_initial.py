# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claims',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ctx_left', models.CharField(max_length=255, verbose_name='Left Context Value', blank=True)),
                ('selected', models.CharField(max_length=255, verbose_name='Selected Text')),
                ('ctx_right', models.CharField(max_length=255, verbose_name='Right Context Value', blank=True)),
                ('status', models.IntegerField(max_length=1, verbose_name='Status of the Claim', choices=[(1, 'New'), (2, 'Assigned'), (3, 'Fixed'), (4, 'Invalid')])),
                ('status_applied', models.DateTimeField(auto_now_add=True, verbose_name='Status Applied')),
                ('comment', models.TextField(verbose_name="Reader's Comment")),
                ('reply', models.TextField(verbose_name='Enter here the reply for the Reader', blank=True)),
                ('url', models.URLField(verbose_name='Context URL')),
                ('email', models.EmailField(max_length=75, verbose_name="Reader's E-mail")),
                ('notify', models.BooleanField(default=False, verbose_name='Reader wants the Notify')),
                ('reg_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Registered')),
            ],
            options={
                'ordering': ('-status_applied',),
                'verbose_name': 'Claim',
                'verbose_name_plural': 'Claims',
            },
            bases=(models.Model,),
        ),
    ]
