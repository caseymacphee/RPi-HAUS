from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from haus.models import Device, Atom, Data
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

    def test_get_day_of_data(self):
        device = Device.objects.first()
        Atom.objects.create(device=device, atom_name="atom_one")
        atom = Atom.objects.first()
        now = datetime.utcnow()
        six_hours_ago = datetime.utcnow() - timedelta(hours=1)
        two_days_ago = datetime.utcnow() - timedelta(days=2)
        now_utc = now.strftime('%s')
        six_hours_ago_utc = six_hours_ago.strftime('%s')
        two_days_ago_utc = two_days_ago.strftime('%s')
        Data.objects.create(atom=atom, value=1, timestamp=now_utc)
        Data.objects.create(atom=atom, value=2, timestamp=six_hours_ago_utc)
        Data.objects.create(atom=atom, value=3, timestamp=two_days_ago_utc)
        client = Client()
        client.login(username="admin", password="admin")
        response = client.get('/devices/%d/atom/%d/' % (device.pk, atom.pk))
        self.assertContains(response, now_utc)
        self.assertContains(response, six_hours_ago_utc)
        self.assertNotContains(response, two_days_ago_utc)

    def test_device_list_permissions(self):
        client = Client()
        client.login(username="regular_user", password="password")
        response = client.get('/devices/')
        self.assertNotContains(response, "testdevice")

    # def test_atom_list_permissions(self):
    #     client = Client()
    #     client.login(username="regular_user", password="password")
    #     response = client.get('/devices/')
    #     self.assertNotContains(response, "testdevice")
