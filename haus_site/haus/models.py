from django.db import models
from django.contrib.auth.models import User


DEVICE_TYPE_CHOICES = (
    ('monitor', 'Monitor Device'),
    ('controller', 'Controller Device')
)


## Ex: Weather Monitor (arduino)
class Device(models.Model):

    def __unicode__(self):
        return self.device_name

    device_name = models.CharField(default='', max_length=200)
    user = models.ForeignKey(User, related_name="devices")
    device_type = models.CharField(choices=DEVICE_TYPE_CHOICES,
                                   max_length=20)

    class Meta:
        unique_together = ('device_name', 'user')


## Ex: Temperature Sensor, Light Switch (each key from arduino)
class Atom(models.Model):

    def __unicode__(self):

        return self.atom_name

    atom_name = models.CharField(default='', max_length=200)
    device = models.ForeignKey(Device, default=None, related_name="atoms")
    unit = models.CharField(default='', max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('atom_name', 'device')


## value from key-value pair
class Data(models.Model):
    atom = models.ForeignKey(Atom, default=None)
    value = models.DecimalField(max_digits=100, decimal_places=10)
    timestamp = models.DecimalField(max_digits=20, decimal_places=4)


class CurrentData(models.Model):
    atom = models.ForeignKey(Atom, default=None)
    value = models.DecimalField(max_digits=10, decimal_places=5)


class DailySummaryData(models.Model):
    atom = models.ForeignKey(Atom, default=None)
    avg_value = models.DecimalField(max_digits=10, decimal_places=5)
    day = models.DateField()


class DeviceUsers(models.Model):

    def __unicode__(self):
        return self.user.username

    user = models.ForeignKey(User, related_name="device_users")
    device_name = models.CharField(default='', max_length=200)
    device_superuser = models.BooleanField(default=False)
    # "following" is implicit by existing in this table
