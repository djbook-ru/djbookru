# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claims',
            name='email',
            field=models.EmailField(max_length=254, verbose_name="Reader's E-mail"),
        ),
        migrations.AlterField(
            model_name='claims',
            name='status',
            field=models.IntegerField(verbose_name='Status of the Claim', choices=[(1, 'New'), (2, 'Assigned'), (3, 'Fixed'), (4, 'Invalid')]),
        ),
    ]
