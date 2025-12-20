import jdatetime
from django import template

register = template.Library()

PERSIAN_MONTHS = [
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
]
@register.filter
def jalali_datetime(value):
    if not value:
        return ""
    return jdatetime.datetime.fromgregorian(datetime=value).strftime("%H:%M:%S %Y/%m/%d")


@register.filter
def jalali_date(value):
    if not value:
        return ""
    return jdatetime.datetime.fromgregorian(datetime=value).strftime("%Y/%m/%d")

@register.filter
def jalali_format(value):
    if not value:
        return ""
    # اگر مقدار از نوع jdatetime باشد، فقط فرمتش را تنظیم می‌کنیم
    try:
        return value.strftime("%H:%M:%S %Y/%m/%d")
    except Exception:
        return str(value)

@register.filter
def jalali_date_fmt(value):
    if not value:
        return ""

    try:
        jdate = jdatetime.date.fromgregorian(date=value)
        return f"{value.day} {PERSIAN_MONTHS[jdate.month - 1]} {value.year}"
    except Exception:
        return str(value)