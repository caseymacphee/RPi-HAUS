from django.test import TestCase, Client
from django.contrib.auth.models import User
# Create your tests here.

from haus.models import Device


class DeviceAPITests(TestCase):
    def setUp(self):
        superuser = User.objects.create_superuser("admin", "", "admin")
        Device.objects.create(name="testdevice", user=superuser, serialpath='',
                              device_type="monitor")

    def test_existing_device_is_retrieved(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future
        """
        client = Client()
        client.login(username="admin", password="admin")
        response = client.get('/devices/')
        # raise Exception(str(dir(response)))
        self.assertIn("testdevice", response.content)
