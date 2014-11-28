from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User
# Create your tests here.

from haus.models import Device
import json


class DeviceAPITests(TestCase):
    def setUp(self):
        superuser = User.objects.create_superuser("admin", "", "admin")
        Device.objects.create(device_name="testdevice", user=superuser,
                              device_type="monitor")
        regular_user = User.objects.create_user("regular_user", "", "password")
        Device.objects.create(device_name="seconddevice", user=regular_user,
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
        self.assertContains(response, "testdevice", status_code=200)
        self.assertNotContains(response, "seconddevice")

    def test_other_user(self):
        client = Client()
        client.login(username="regular_user", password="password")
        response = client.get('/devices/')
        self.assertContains(response, "seconddevice")

    def test_create_device(self):
        client = Client()
        client.login(username="admin", password="admin")
        device_data = {"device_name": "Admin Device", "device_type": "monitor",
                       "atoms": []}
        response = client.post('/devices/', data=device_data)
        self.assertContains(response, "Admin Device", status_code=201)
        devicedata = json.loads(response.content)
        device = Device.objects.get(pk=devicedata['id'])
        self.assertEqual(device.device_name, "Admin Device")

    def test_update_device(self):
        client = Client()
        client.login(username="admin", password="admin")
        response = client.get('/devices/')
        devicedata = json.loads(response.content)[0]
        oldname = devicedata['device_name']
        updated_data = {'device_name': "Newname",
                        'id': devicedata['id'],
                        'device_type': devicedata['device_type'],
                        'atoms': devicedata['atoms'],
                        }
        client.post('/devices/', data=updated_data)
        new_device_list = client.get('/devices/')
        self.assertContains(new_device_list, "Newname")
        self.assertNotContains(new_device_list, oldname)

    def test_post_atom_data(self):
        atomdata = json.dumps({"timestamp": "5.5",
                               "atoms": {"sats": "0", "date": "00/-1/2000",
                                         "tempf": "71.7"}
                               })
        client = Client()
        client.login(username="admin", password="admin")
        response = client.get('/devices/')
        devicedata = json.loads(response.content)[0]
        response = client.post('/devices/%d/' % devicedata['id'],
                               content_type='application/json', data=atomdata)
        self.assertContains(response, "tempf", status_code=202)
