# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='example',
            name='is_draft_for',
            field=models.ForeignKey(verbose_name='is draft for', blank=True, to='examples.Example', null=True),
        ),
    ]
