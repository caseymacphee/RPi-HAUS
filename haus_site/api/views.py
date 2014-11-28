# from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView
from api.serializers import DeviceSerializer, AtomSerializer, DataSerializer, CurrentDataSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from haus.models import Device, Atom, CurrentData
from copy import copy


class DeviceListView(APIView):

    def get(self, request, format=None):
        devices = Device.objects.filter(user_id=request.user.pk)
        device_serializer = DeviceSerializer(devices, many=True)
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

    # From the URL, we get the device_id and the atom_id
    def get(self, request, device_pk, atom_pk, format=None):
        current_data = self.get_current_data_object(atom_pk)
        current_data_serializer = CurrentDataSerializer(current_data)
        return Response(current_data_serializer.data)

    def get_current_data_object(self, atom_pk):

        try:

            return CurrentData.objects.get(atom=atom_pk)

        except CurrentData.DoesNotExist:

            return None



class CurrentDeviceView(APIView):


    def get(self, request, device_pk, format=None):

        device = self.get_device_object(request, device_pk)

        #print str(device.atoms.devices.all())

        # for each_atom in device.atoms.filter

        #     print each_atom

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








