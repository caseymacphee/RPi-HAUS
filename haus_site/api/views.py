# from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView
from api.serializers import DeviceSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status


class DeviceListView(APIView):

    def get(self, request, format=None):
        devices = request.user.devices.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DeviceSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceDetailView(APIView):

    # NOTE: Unlike in the tutorial, request is passed to get_object()
    # because we're not currently importing models. We can import models
    # and change the query from request.....get() to a more direct model query.
    def get_object(self, request, device_pk):
        try:
            # This is based on the assumption that users can only see
            # devices that include those users as owners. (nb reverse relation)
            # Should this assumption be changed, this code must change as well:
            return request.user.devices.get(pk=device_pk)
        # The tutorial recommended specifically excepting on their model's
        # DoesNotExist class (which our model would have too, if it was
        # imported here, which is isn't right now).
        except:
            raise Http404

    def get(self, request, device_pk, format=None):
        device = self.get_object(request, device_pk)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def put(self, request, device_pk, format=None):
        device = self.get_object(request, device_pk)
        serializer = DeviceSerializer(device, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # url(r'^devices/(?P<device_pk>[0-9]+)/$',
    #     views.DeviceView.as_view()),  # Get device info, put device data
    # url(r'^devices/(?P<device_pk>[0-9]+)/current/$',
    #     views.CurrentDeviceView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/$',
    #     views.AtomView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/current/$',
    #     views.CurrentAtomView.as_view()),
