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
    url(r'^devices/$', views.DeviceListView.as_view()),
    url(r'^devices/(?P<device_pk>[0-9]+)/$',
        views.DeviceDetailView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/current/$',
    #     views.CurrentDeviceView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/$',
    #     views.AtomView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/current/$',
    #     views.CurrentAtomView.as_view()),
)
