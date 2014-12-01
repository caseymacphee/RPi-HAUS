# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haus', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentdata',
            name='value',
            field=models.DecimalField(max_digits=100, decimal_places=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dailysummarydata',
            name='avg_value',
            field=models.DecimalField(max_digits=100, decimal_places=10),
            preserve_default=True,
        ),
    ]
