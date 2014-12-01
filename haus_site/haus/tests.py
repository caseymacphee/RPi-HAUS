from django.test import TestCase
from cron_jobs import daily_summary_cron
from datetime import datetime, timedelta
from models import Device, Atom, Data, DailySummaryData, User

class CronTest(TestCase):
    def setUp(self):
        superuser = User.objects.create_superuser("admin", "", "admin")
        Device.objects.create(device_name="testdevice", user=superuser,
                              device_type="monitor")

        device = Device.objects.first()
        Atom.objects.create(device=device, atom_name="atom_one")
        atom = Atom.objects.first()
        now = datetime.utcnow()
        today = datetime(now.year, now.month, now.day)
        yesterday = (today - timedelta(hours=12)).strftime('%s')
        two_days_ago1 = (today - timedelta(days=1, hours=6)).strftime('%s')
        two_days_ago2 = (today - timedelta(days=1, hours=18)).strftime('%s')
        three_days_ago = (today - timedelta(days=2, hours=12)).strftime('%s')
        now_utc = now.strftime('%s')
        Data.objects.create(atom=atom, value=1, timestamp=now_utc)
        Data.objects.create(atom=atom, value=2, timestamp=two_days_ago1)
        Data.objects.create(atom=atom, value=3, timestamp=two_days_ago2)
        Data.objects.create(atom=atom, value=4, timestamp=three_days_ago)
        Data.objects.create(atom=atom, value=5, timestamp=yesterday)
    
    def test_daily_summary_cron(self):
        daily_summary_cron()
        dsd = DailySummaryData.objects.first()
        avg = dsd.avg_value
        day = dsd.day
        now = datetime.utcnow()
        yesterday = (now - timedelta(days=1))
        yesterday_trunc = datetime(yesterday.year,
                                   yesterday.month,
                                   yesterday.day, 0).strftime('%s')
        self.assertEquals(avg, 2.5)
        self.assertEqual(day, float(yesterday_trunc))
