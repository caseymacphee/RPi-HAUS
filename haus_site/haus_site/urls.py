from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'haus_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^devices/$', views.DeviceListView),  # Returns device list & atoms.
    # url(r'^devices/(?P<device_pk>[0-9]+)/$',
    #     views.DeviceView.as_view()),  # Returns device info, takes device data
    # url(r'^devices/(?P<device_pk>[0-9]+)/current/$',
    #     views.CurrentDeviceView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/$',
    #     views.AtomView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/current/$',
    #     views.CurrentAtomView.as_view()),
)
