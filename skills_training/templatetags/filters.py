from django import template
import re
import jdatetime

register = template.Library()

@register.filter
def safe_slug(value):
    """
    تبدیل نام دسته‌بندی به رشته‌ای امن برای data-category
    فاصله -> _ 
    حروف فارسی و انگلیسی + اعداد نگه داشته می‌شوند
    """
    value = str(value).strip()
    value = re.sub(r'\s+', '_', value)          # فاصله‌ها را با _ جایگزین کن
    value = re.sub(r'[^\w\u0600-\u06FF_]', '', value)  # فقط حروف، اعداد و _ نگه دار
    return value


@register.filter
def gregorian_to_jalali(value):
    if value:
        try:
            return jdatetime.date.fromgregorian(date=value).strftime("%Y/%m/%d")
        except:
            return value
    return "-"