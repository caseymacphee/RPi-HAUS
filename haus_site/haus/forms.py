from django import forms
from registration.forms import RegistrationForm
import models


class CreateDevicePermissionForm(forms.ModelForm):

    class Meta:
        model = models.DevicePermission
        fields = ['user', 'device', 'device_name', 'device_superuser']


class EditDevicePermissionForm(forms.ModelForm):

    class Meta:
        model = models.DevicePermission
        fields = ['user', 'device', 'device_name', 'device_superuser']


class DeleteDevicePermissionForm(forms.ModelForm):

    class Meta:
        model = models.DevicePermission
        fields = ['user', 'device']


