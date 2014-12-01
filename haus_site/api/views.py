# from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView
from api.serializers import DeviceSerializer, AtomSerializer, DataSerializer, CurrentDataSerializer
from rest_framework.response import Response
from django.http import Http404, HttpResponseForbidden
from rest_framework import status
from haus.models import Device, Atom, CurrentData, Data, DevicePermission
from copy import copy
from datetime import datetime, timedelta


class DeviceListView(APIView):
    # (Not a good docstring, but important for testing.)
    """
    To add a new device during setup, the following view
    expects data that looks like this:
    {"device_name": "testdevice0",
     "device_type": "monitor"}
    """

    def get(self, request, format=None):

        # When a Device is created a DevicePermission will also
        # be created for the User who created that Device.
        # devices_owned_by_user = Device.objects.filter(user_id=request.user.pk)

        # Adding listing of Devices a User has a DevicePermission for.
        permissions = DevicePermission.objects.filter(user=request.user.pk)

        # Each DevicePermission has a Device, and each Device has a pk:
        permitted_device_pks = [permission.device.pk for permission in permissions.all()]

        # With the above info, we can compile a list of Device objects
        # from the database that the User has a DevicePermission for:
        devices_user_is_permitted_for = []
        for each_device_pk in permitted_device_pks:
            device_to_append = Device.objects.get(pk=each_device_pk)
            devices_user_is_permitted_for.append(device_to_append)

        device_serializer = DeviceSerializer(devices_user_is_permitted_for,
                                             many=True)

        return Response(device_serializer.data)

    def post(self, request, format=None):

        # print("\nRequest == " + str(dir(request)))

        # print(request.user.id)

        device = self.get_device_object(request)

        requestdata = copy(request.DATA)

        requestdata['user'] = request.user.id

        device_serializer = DeviceSerializer(device, data=requestdata)

        # print "\nrequest.DATA == " + str(request.DATA)

        # print(device_serializer.is_valid())

        # print device_serializer.attributes()

        if device_serializer.is_valid():
            device_serializer.save()
            device = self.get_device_object(request)

            # Assuming atoms value is a list of atom names
            # atom_names = request.DATA['atoms']
            # print (str("atom_names == " + str(atom_names)))
            # for atom_name in atom_names:
            # print atom_name
            # atom = self.get_atom_object(atom_name, device)
            # print("atom == " + str(atom))
            # atom_data = {'name': atom_name, 'device': device.pk}
            # print("atom_data == " + str(atom_data))
            # atom_serializer = AtomSerializer(atom, data=atom_data)
            # print("atom_serializer == " + str(dir(atom_serializer)))

            # for each_dirname in dir(atom_serializer):
            #    print str(each_dirname) + ": " + (str(getattr(atom_serializer, each_dirname)))

            # if atom_serializer.is_valid():
            # print("atom_serializer.is_valid == True")
            # atom_serializer.save()

            if device_serializer.was_created is True:
                # If a Device was actually created in the serializer, we need
                # to give the User a DevicePermission as well.
                # This should NOT be done in views.py -- it's in models.py,
                # and accomplished by adding a create() method to the
                # Device class, which is called in serializers.py in lieu of
                # calling the Device class outright.
                return Response(device_serializer.data, status=status.HTTP_201_CREATED)
            elif device_serializer.was_created is False:
                return Response(device_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_device_object(self, request):
        print str(request.DATA)
        if request.DATA.get('id', None):

            try:
                return Device.objects.filter(user=request.user.id, id=request.DATA['id'])[0]

            except Device.DoesNotExist:
                return None

        else:

            try:
                return Device.objects.filter(user=request.user.id, device_name=request.DATA['device_name']).first()

                #print("device_pk == " + str(device_pk))

                # This is based on the assumption that users can only see
                # devices that include those users as owners. (nb reverse relation)
                # Should this assumption be changed, this code must change as well:
                # return request.user.devices.get(pk=device_pk)

                # Now changed to models and open-access:
                # return Device.objects.get(pk=device_pk)

            except Device.DoesNotExist:
                # The device must then be made inside the device_serializer,
                # which is expecting None.
                return None

    # def put(self, request, device_pk, format=None):
    #     device = self.get_device_object(device_pk)
    #     device_serializer = DeviceSerializer(device, data=request.DATA)

    #     if device_serializer.is_valid():
    #         device_serializer.save()
    #         return Response(device_serializer.data)
    #     return Response(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentAtomView(APIView):

    def get_atom_object(self, atom_pk):

        try:
            return Atom.objects.get(pk=atom_pk)

        except Atom.DoesNotExist:
            return None

    def get_permission_for_device(self, request, device):

        try:
            # We're trying to return a permission ONLY IF
            # there is a permission for this device for this user.
            current_user = request.user.id
            return DevicePermission.objects.get(device=device,
                                                user=current_user)

        except DevicePermission.DoesNotExist:
            return None

    def get_permission_for_atom(self, request, atom_pk):

        the_atom_in_question = self.get_atom_object(atom_pk)
        if the_atom_in_question is not None:
            device_of_this_atom = the_atom_in_question.device

            permission = self.get_permission_for_device(request, device_of_this_atom)

            return permission

    # From the URL, we get the device_id and the atom_id
    def get(self, request, device_pk, atom_pk, format=None):

        permission = self.get_permission_for_atom(request, atom_pk)

        if not permission:
            return HttpResponseForbidden("You do not have permission to view this atom.")

        else:
            current_data = self.get_current_data_object(atom_pk)
            current_data_serializer = CurrentDataSerializer(current_data)
            return Response(current_data_serializer.data)

    def get_current_data_object(self, atom_pk):

        try:

            return CurrentData.objects.get(atom=atom_pk)

        except CurrentData.DoesNotExist:

            return None


class CurrentDeviceView(APIView):

    def get_permission_for_device(self, request, device):

        try:
            # We're trying to return a permission ONLY IF
            # there is a permission for this device for this user.
            current_user = request.user.id
            return DevicePermission.objects.get(device=device,
                                                user=current_user)

        except DevicePermission.DoesNotExist:
            return None

    def get(self, request, device_pk, format=None):

        device = self.get_device_object(request, device_pk)

        permission = self.get_permission_for_device(request, device)
        if not permission:
            # Break the function and 403 if the user does not have permission:
            return HttpResponseForbidden("You do not have permission to view this device.")

        # If the user does have permission, continue as normal.
        list_of_atoms = device.atoms.all()

        current_data_serializer_list = []

        for each_atom in list_of_atoms:

            if each_atom.device.user.id == request.user.id:

                current_data_object = self.get_current_data_object(each_atom.pk)
                current_data_serializer = CurrentDataSerializer(current_data_object)
                current_data_serializer_list.append(current_data_serializer.data)

        return Response(current_data_serializer_list)

    def get_current_data_object(self, atom_pk):

        try:

            return CurrentData.objects.get(atom=atom_pk)

        except CurrentData.DoesNotExist:

            return None

    def get_device_object(self, request, device_pk):

        try:
            return Device.objects.filter(user=request.user.id, pk=device_pk).first()

            #print("device_pk == " + str(device_pk))

            # This is based on the assumption that users can only see
            # devices that include those users as owners. (nb reverse relation)
            # Should this assumption be changed, this code must change as well:
            # return request.user.devices.get(pk=device_pk)

            # Now changed to models and open-access:
            # return Device.objects.get(pk=device_pk)

        except Device.DoesNotExist:
            # The device must then be made inside the device_serializer,
            # which is expecting None.
            return None






class DeviceDetailView(APIView):
    # (Not a good docstring, but important for testing.)
    """
    To update the data (also adds atoms to a device),
    the following view expects data that looks like this:
    {"atoms":
        {"AtomName": 325,
         "AnotherAtomName": 465},
     "timestamp": 93432432}
    """




    # NOTE: Unlike in the tutorial, request is passed to get_device_object()
    # because we're not currently importing models. We can import models
    # and change the query from request.....get() to a more direct model query.
    def get_device_object(self, device_pk):
        try:
            # This is based on the assumption that users can only see
            # devices that include those users as owners. (nb reverse relation)
            # Should this assumption be changed, this code must change as well:
            # return request.user.devices.get(pk=device_pk)

            # Now changed to models and open-access:
            return Device.objects.get(pk=device_pk)

        except Device.DoesNotExist:
            raise Http404

    def get_atom_object(self, atom_name, device):

        try:

            return Atom.objects.filter(atom_name=atom_name, device=device).first()

        except Atom.AtomDoesNotExist:

            return None

    def get_current_data_object(self, atom_pk):

        try:

            return CurrentData.objects.get(atom=atom_pk)

        except CurrentData.DoesNotExist:

            return None

    def get(self, request, device_pk, format=None):
        device = self.get_device_object(device_pk)
        device_serializer = DeviceSerializer(device)
        return Response(device_serializer.data)

    # def put(self, request, device_pk, format=None):
    #     device = self.get_device_object(device_pk)
    #     request.DATA['user_id'] = request.user.id
    #     device_serializer = DeviceSerializer(device, data=request.DATA)

    #     if device_serializer.is_valid():
    #         device_serializer.save()
    #         return Response(device_serializer.data)
    #     return Response(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, device_pk, format=None):

        # print("\nRequest == " + str(dir(request)))

        # print(request.user.id)

        device_object = self.get_device_object(device_pk)
        # device_serializer = DeviceSerializer(device, data=request.DATA)

        # print "\nrequest.DATA == " + str(request.DATA)

        # print(device_serializer.is_valid())

        # print device_serializer.attributes()

        # request.DATA['atoms'] now contains a dictionary of atom:value pairs:
        atom_dictionary = request.DATA['atoms']
        timestamp = request.DATA['timestamp']

        atom_serializer_list = []

        # print (str("atom_names == " + str(atom_names)))
        for atom_key, atom_value in atom_dictionary.iteritems():
            # print atom_name
            atom_object = self.get_atom_object(atom_key, device_object)
            # print("atom == " + str(atom))
            atom_data = {'atom_name': atom_key, 'value': atom_value, 'device': device_object.pk, 'timestamp': timestamp}
            # print("atom_data == " + str(atom_data))
            atom_serializer = AtomSerializer(atom_object, data=atom_data)
            # print("atom_serializer == " + str(dir(atom_serializer)))

            # for each_dirname in dir(atom_serializer):
            #    print str(each_dirname) + ": " + (str(getattr(atom_serializer, each_dirname)))

            if atom_serializer.is_valid():
                # print("atom_serializer.is_valid == True")
                atom_serializer_list.append(atom_serializer)

            else:
                return Response(atom_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data_to_return = []

        for each_atom_serializer in atom_serializer_list:

            each_atom_serializer.save()

            data_to_return.append(each_atom_serializer.data)

        for atom_key, atom_value in atom_dictionary.iteritems():

            atom_object = self.get_atom_object(atom_key, device_object)

            data_data = {'value': atom_value, 'atom': atom_object.pk, 'timestamp': timestamp}

            data_serializer = DataSerializer(data=data_data)

            print(str(atom_key) + ", " + str(atom_value) + " == " + str(data_serializer.is_valid()))

            print(str(data_serializer.errors))

            if data_serializer.is_valid():

                data_serializer.save()

                atom_pk = atom_object.pk

                current_data_object = self.get_current_data_object(atom_pk)

                current_data_serializer = CurrentDataSerializer(current_data_object, data=data_data)

                if current_data_serializer.is_valid():

                    current_data_serializer.save()

        return Response(data_to_return, status=status.HTTP_202_ACCEPTED)


class DataView(APIView):

    def get(self, request, device_pk, atom_pk, format=None):
        # get data from last 24 hours
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        one_day_ago_uni = one_day_ago.strftime('%s')
        data = Data.objects.filter(atom_id=atom_pk,
                                   timestamp__gt=one_day_ago_uni)
        data_serializer = DataSerializer(data, many=True)
        return Response(data_serializer.data)





