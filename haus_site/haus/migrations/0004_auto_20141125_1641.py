# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haus', '0003_auto_20141125_1618'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='atom',
            unique_together=set([('name', 'device')]),
        ),
    ]
