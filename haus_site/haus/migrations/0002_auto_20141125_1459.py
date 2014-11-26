# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haus', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('name', 'user')]),
        ),
    ]
