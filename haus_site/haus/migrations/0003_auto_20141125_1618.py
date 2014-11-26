# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haus', '0002_auto_20141125_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atom',
            name='unit',
            field=models.CharField(default=b'', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
