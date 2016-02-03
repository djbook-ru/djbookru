# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0002_add_related_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='usersocialauth',
            name='user',
            field=models.ForeignKey(related_name='social_auth', to='accounts.User'),
        ),
    ]
