from models import Data, DailySummaryData, Atom
from datetime import datetime

# take data from time a to time b, average, and add a daily value


def daily_summary_cron():
    now = datetime.utcnow()
    yesterday = datetime(now.year, now.month, now.day - 1, 0)
    two_days_ago = datetime(now.year, now.month, now.day - 2, 0)
    yesterday_uni = yesterday.strftime('%s')
    two_days_ago_uni = two_days_ago.strftime('%s')

    atoms = Atom.objects.all()
    for atom in atoms:
        day_data_objs = Data.objects.filter(timestamp__gt=two_days_ago_uni,
                                        timestamp__lt=yesterday_uni, atom=atom)
        day_data_list = [data.value for data in day_data_objs]
        day_avg = sum(day_data_list) / len(day_data_list)
        DailySummaryData.objects.create(atom=atom, avg_value=day_avg,
                                        day=yesterday)
