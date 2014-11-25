# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from api.serializers import UserSerializer, GroupSerializer
from api.serializers import DeviceSerializer
from api.models import Device


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DeviceListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DeviceSerializer

    def get(self, request, format=None):
        devices = request.user.devices.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)


    # url(r'^devices/(?P<device_pk>[0-9]+)/$',
    #     views.DeviceView.as_view()),  # Returns device info, takes device data
    # url(r'^devices/(?P<device_pk>[0-9]+)/current/$',
    #     views.CurrentDeviceView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/$',
    #     views.AtomView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/current/$',
    #     views.CurrentAtomView.as_view()),


# class DataView(generics.ListCreateAPIView):
#     serializer_class = TimeSeriesSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def get_queryset(self):
#         """
#         This view should return a list of all the data points
#         for the currently authenticated user.
#         """
#         user = self.request.user
#         return TimeSeries.objects.filter(owner=user)

#     def pre_save(self, obj):
#         obj.owner = self.request.user


# class DataDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TimeSeries.objects.all()
#     serializer_class = TimeSeriesSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def pre_save(self, obj):
#         obj.owner = self.request.user
