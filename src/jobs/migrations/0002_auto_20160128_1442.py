# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='company_name_slug',
            field=models.SlugField(max_length=255, null=True, verbose_name='company name slug'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='description',
            field=models.TextField(help_text='Use <a target="blank"href="http://daringfireball.net/projects/markdown/syntax">Markdown</a> and HTML', verbose_name='job description'),
        ),
    ]
