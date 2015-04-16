# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import src.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userrepository'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                (b'objects', src.accounts.models.UserManager()),
            ],
        ),
    ]
