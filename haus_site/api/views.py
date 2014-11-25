# from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView
from api.serializers import DeviceSerializer
from rest_framework.response import Response


class DeviceListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DeviceSerializer

    def get(self, request, format=None):
        devices = request.user.devices.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)


    # url(r'^devices/(?P<device_pk>[0-9]+)/$',
    #     views.DeviceView.as_view()),  # Get device info, put device data
    # url(r'^devices/(?P<device_pk>[0-9]+)/current/$',
    #     views.CurrentDeviceView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/$',
    #     views.AtomView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/current/$',
    #     views.CurrentAtomView.as_view()),
