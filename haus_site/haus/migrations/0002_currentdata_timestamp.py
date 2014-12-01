# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentdata',
            name='timestamp',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=4),
            preserve_default=False,
        ),
    ]
