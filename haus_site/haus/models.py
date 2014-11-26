from django.db import models
from django.contrib.auth.models import User


DEVICE_TYPE_CHOICES = (
    ('monitor', 'Monitor Device'),
    ('controller', 'Controller Device')
)


# class HausUser(User):
#     pass


# Ex: Weather Monitor (arduino)
class Device(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(default='', max_length=200)
    user = models.ForeignKey(User, related_name="devices")
    serialpath = models.CharField(max_length=200, default='')
    device_type = models.CharField(choices=DEVICE_TYPE_CHOICES,
                                   max_length=20)

    class Meta:
        unique_together = ('name', 'user')


# Ex: Temperature Sensor, Light Switch (each key from arduino)
class Atom(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(default='', max_length=200)
    device = models.ForeignKey(Device, default=None, related_name="atoms")
    unit = models.CharField(default='', max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('name', 'device')


# value from key-value pair
class Data(models.Model):
    atom = models.ForeignKey(Atom, default=None)
    value = models.DecimalField(max_digits=10, decimal_places=5)
    timestamp = models.DateTimeField(db_index=True, auto_now=True)


class CurrentData(models.Model):
    atom = models.ForeignKey(Atom, default=None)
    value = models.DecimalField(max_digits=10, decimal_places=5)


class DailySummaryData(models.Model):
    atom = models.ForeignKey(Atom, default=None)
    avg_value = models.DecimalField(max_digits=10, decimal_places=5)
    day = models.DateField()
