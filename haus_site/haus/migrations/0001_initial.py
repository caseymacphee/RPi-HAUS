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
                ('atom_name', models.CharField(default=b'', max_length=200)),
                ('unit', models.CharField(default=b'', max_length=20, null=True, blank=True)),
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
                ('value', models.DecimalField(max_digits=100, decimal_places=10)),
                ('timestamp', models.DecimalField(max_digits=20, decimal_places=4)),
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
                ('device_name', models.CharField(default=b'', max_length=200)),
                ('device_type', models.CharField(max_length=20, choices=[(b'monitor', b'Monitor Device'), (b'controller', b'Controller Device')])),
                ('user', models.ForeignKey(related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_name', models.CharField(default=b'', max_length=200)),
                ('device_superuser', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='device_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('device_name', 'user')]),
        ),
        migrations.AddField(
            model_name='atom',
            name='device',
            field=models.ForeignKey(related_name='atoms', default=None, to='haus.Device'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='atom',
            unique_together=set([('atom_name', 'device')]),
        ),
    ]
