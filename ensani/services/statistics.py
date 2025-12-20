import jdatetime
from soldiers.models import Soldier
from datetime import datetime, time
from django.utils.timezone import localtime, make_aware


def get_paziresh_peak_multi_day(
    start_jdate: jdatetime.date,
    end_jdate: jdatetime.date,
):
    """
    خروجی:
    {
        labels: [0..23],
        datasets: [
            { label: '1404/10/01', data: [..24..] },
            ...
        ]
    }
    """

    # تبدیل بازه جلالی به datetime دقیق
    start_dt = make_aware(
        datetime.combine(start_jdate.togregorian(), time.min)
    )
    end_dt = make_aware(
        datetime.combine(end_jdate.togregorian(), time.max)
    )

    queryset = Soldier.objects.filter(
        tarikh_paziresh__gte=start_dt,
        tarikh_paziresh__lte=end_dt,
    ).only('tarikh_paziresh')


    def frmd(date):
        return date.strftime("%Y/%m/%d")
    # لیست روزهای جلالی
    days = []
    d = start_jdate
    while d <= end_jdate:
        days.append(d)
        d += jdatetime.timedelta(days=1)

    daily_hourly = {frmd(day): [0] * 25 for day in days}

    for soldier in queryset:
        tp = soldier.tarikh_paziresh
        if not tp:
            continue
        
        day_key = frmd(tp)
        hour    = tp.hour
        if day_key in daily_hourly:
            daily_hourly[day_key][hour] += 1
        else:
            daily_hourly[day_key] = [0] * 25 
            daily_hourly[day_key][hour] = 1

    labels = list(range(25))

    datasets = [
        {
            "label": frmd(day) ,
            "data": daily_hourly[frmd(day)]
        }
        for day in days
    ]

    return {
        "labels": labels,
        "datasets": datasets
    }
