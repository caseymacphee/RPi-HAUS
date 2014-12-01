from models import Data, DailySummaryData, Atom
from datetime import datetime, timedelta

# take data from time a to time b, average, and add a daily value


def daily_summary_cron():
    """
    Run a cron job to insert summary of yesterday's data into the
    DailySummaryData model.
    timestamp will be UTC of yesterday (today's date - one day), hour 0
    """
    now = datetime.utcnow()
    today = datetime(now.year, now.month, now.day)
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    yesterday_uni = yesterday.strftime('%s')
    two_days_ago_uni = two_days_ago.strftime('%s')

    atoms = Atom.objects.all()
    print atoms
    for atom in atoms:
        day_data_objs = Data.objects.filter(timestamp__gt=two_days_ago_uni,
                                        timestamp__lt=yesterday_uni, atom=atom)
        day_data_list = [data.value for data in day_data_objs]
        print day_data_list
        if day_data_list:
            day_avg = sum(day_data_list) / len(day_data_list)
        else:
            day_avg = 0

        DailySummaryData.objects.create(atom=atom, avg_value=day_avg,
                                        day=yesterday_uni)
