# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haus', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DailySummaryData',
        ),
        migrations.CreateModel(
            name='DailySummaryData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avg_value', models.DecimalField(max_digits=10, decimal_places=5)),
                ('day', models.DecimalField(max_digits=20, decimal_places=4)),
                ('atom', models.ForeignKey(default=None, to='haus.Atom')),
            ],
            options={
            },
            bases=(models.Model,),
        )
    ]
