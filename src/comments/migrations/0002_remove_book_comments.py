# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_book_comments(apps, schema_editor):
    Comment = apps.get_model('comments', 'Comment')
    Comment.objects.filter(content_type__app_label='main').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
        # ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(remove_book_comments, migrations.RunPython.noop),
    ]
