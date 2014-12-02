from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from forms import CreateDevicePermissionForm
from models import DevicePermission


# Create your views here.

@login_required
def home(request):
    return render(request, 'haus/dataview.html', None)


@login_required
def add_device_permission(request):

    # Untested as of Dec 1st 2014. MAY work if you make it match the frontend.

    if request.method == 'POST':

        permission_form = CreateDevicePermissionForm(request.POST)

        if permission_form.is_valid():

            # get_user_model() is more Djangolic.
            submitting_user = get_object_or_404(get_user_model(),
                                                pk=request.user.id)
            device = permission_form.cleaned_data['device']

            # Check whether this user is allowed to edit permissions:
            if device.user != submitting_user:
                return render(request, 'haus/dataview.html', None)

            new_device_permission = DevicePermission.objects.create(
                user=permission_form.cleaned_data['user'],
                device=permission_form.cleaned_data['device'],
                device_name=permission_form.cleaned_data['device_name'],
                device_superuser=permission_form.cleaned_data['device_superuser']
                )

            new_device_permission.save()

        return render(request, 'haus/dataview.html', None)

    else:

        permission_form = CreateDevicePermissionForm()

    return render(request, 'haus/dataview.html', None)



def delete_device_permission(request):

    # Does not work. Too bad.

    pass





