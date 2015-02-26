# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeaderMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=2048, verbose_name='Phrase')),
            ],
            options={
                'verbose_name': 'Phrase',
                'verbose_name_plural': 'Phrases',
            },
            bases=(models.Model,),
        ),
    ]
