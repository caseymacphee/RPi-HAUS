from django.conf.urls import patterns, include, url
from django.contrib import admin

from api import views

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'haus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),


    # To add a new device during setup, the following view
    # expects data that looks like this:
    # {"device_name": "testdevice0",
    #  "device_type": "monitor"}
    url(r'^devices/$', views.DeviceListView.as_view()),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^devices/(?P<device_pk>[0-9]+)/$',
    #     views.DeviceView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/current/$',


    # To update the data (also adds atoms to a device),
    # the following view expects data that looks like this:
    # {"atoms":
    #     {"AtomName": 325,
    #      "AnotherAtomName": 465},
    #  "timestamp": 93432432}
    url(r'^devices/(?P<device_pk>[0-9]+)/$',
        views.DeviceDetailView.as_view()),

    url(r'^devices/(?P<device_pk>[0-9]+)/current/$',
        views.CurrentDeviceView.as_view()),


    # url(r'^devices/(?P<device_pk>[0-9]+)/changed/$',
    #     views.CurrentDeviceView.as_view()),


    url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/$',
        views.DataView.as_view()),

    url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/current/$',
        views.CurrentAtomView.as_view()),
)
