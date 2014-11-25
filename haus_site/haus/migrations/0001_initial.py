# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Atom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200)),
                ('unit', models.CharField(default=b'', max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CurrentData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=5)),
                ('atom', models.ForeignKey(default=None, to='haus.Atom')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DailySummaryData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avg_value', models.DecimalField(max_digits=10, decimal_places=5)),
                ('day', models.DateField()),
                ('atom', models.ForeignKey(default=None, to='haus.Atom')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=5)),
                ('timestamp', models.DateTimeField(auto_now=True, db_index=True)),
                ('atom', models.ForeignKey(default=None, to='haus.Atom')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200)),
                ('serialpath', models.CharField(default=b'', max_length=200)),
                ('device_type', models.CharField(max_length=20, choices=[(b'monitor', b'Monitor Device'), (b'controller', b'Controller Device')])),
                ('user', models.ForeignKey(related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='atom',
            name='device',
            field=models.ForeignKey(related_name='atoms', default=None, to='haus.Device'),
            preserve_default=True,
        ),
    ]
