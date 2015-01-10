# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='handle',
            field=models.CharField(max_length=83),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='association',
            name='server_url',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
    ]
