# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('haus', '0002_auto_20141130_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevicePermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_name', models.CharField(default=b'', max_length=200)),
                ('device_superuser', models.BooleanField(default=False)),
                ('device', models.ForeignKey(related_name='permitted_users', to='haus.Device')),
                ('user', models.ForeignKey(related_name='permitted_devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='deviceusers',
            name='user',
        ),
        migrations.DeleteModel(
            name='DeviceUsers',
        ),
        migrations.AlterUniqueTogether(
            name='devicepermission',
            unique_together=set([('user', 'device')]),
        ),
    ]
