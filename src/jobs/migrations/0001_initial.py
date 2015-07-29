# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150416_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('employment_type', models.CharField(default=b'FT', max_length=2, verbose_name='employment type', choices=[(b'FT', 'Full Time'), (b'PT', 'Part Time'), (b'CT', 'Contract')])),
                ('location', models.CharField(max_length=255, verbose_name='location')),
                ('remote_work', models.BooleanField(default=False, verbose_name='remote work?')),
                ('title', models.CharField(max_length=255, verbose_name='job title')),
                ('description', models.TextField(help_text='Formatted with Markdown', verbose_name='job description')),
                ('company_name', models.CharField(max_length=255, verbose_name='company name')),
                ('company_website', models.URLField(verbose_name='company website', blank=True)),
                ('how_to_apply', models.TextField(help_text='For example: Email yourresume to job@exmpl.com', verbose_name='how to apply')),
                ('status', models.CharField(default=b'DRT', max_length=3, verbose_name='status position', choices=[(b'DRT', 'Draft'), (b'PUB', 'Published')])),
                ('pub_date', models.DateField(auto_now_add=True)),
                ('last_edit_date', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(verbose_name='author', to='accounts.User')),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name': 'job',
                'verbose_name_plural': 'jobs',
            },
        ),
    ]
