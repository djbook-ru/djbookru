# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('repo_type', models.PositiveIntegerField(verbose_name='type', choices=[(1, 'GitHub'), (2, 'BitBucket')])),
                ('user_name', models.CharField(max_length=64, verbose_name='login')),
                ('user', models.ForeignKey(verbose_name='user', to='accounts.User')),
            ],
            options={
                'verbose_name': 'user repository',
                'verbose_name_plural': 'user repositories',
            },
            bases=(models.Model,),
        ),
    ]
