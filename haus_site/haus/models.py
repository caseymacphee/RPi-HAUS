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

    @classmethod
    def create(cls, device_name, user, device_type):

        print("    Create was called in models.py")

        # Reference:
        # https://docs.djangoproject.com/
        #     en/dev/ref/models/instances/#creating-objects

        device = cls(device_name=device_name,
                     user=user,
                     device_type=device_type)

        device.save()

        new_device_permission = DevicePermission()
        new_device_permission.user = user
        new_device_permission.device = device
        # NOTE: Users can change their particular DevicePermission's
        # device_name, but it doesn't make sense to do it in Device.create()
        # because the person who gets this particular DevicePermission is
        # already naming it whatever they want. Instead, a view to modify
        # DevicePermissions should include a way to change a particular
        # DevicePermission's device_name field.
        new_device_permission.device_name = device_name
        # This is set to True because they created this Device.
        # Users should be able to control Devices they create.
        new_device_permission.device_superuser = True
        new_device_permission.save()

        return device

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
    value = models.DecimalField(max_digits=100, decimal_places=10)
    timestamp = models.DecimalField(max_digits=20, decimal_places=4)


class DailySummaryData(models.Model):
    atom = models.ForeignKey(Atom, default=None)
    avg_value = models.DecimalField(max_digits=100, decimal_places=10)
    day = models.DecimalField(max_digits=20, decimal_places=4)


class DevicePermission(models.Model):

    def __unicode__(self):
        return self.user.username

    user = models.ForeignKey(User, related_name="permitted_devices")
    device = models.ForeignKey(Device, related_name="permitted_users")
    device_name = models.CharField(default='', max_length=200)
    device_superuser = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'device')
