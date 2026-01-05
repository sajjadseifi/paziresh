
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


@register.filter
def split(value, sep=","):
    return value.split(sep)
@register.filter
def get(value={}, item=''):
    if item in value:
        return value.get(item)
    
    return None;

@register.filter
def is_rank_access(access=None, item=''):
    if access is None:
        access = []
    return item in access

@register.filter
def located_code(value, tatbigh=False):
    return value.located_code(tatbigh=tatbigh)



@register.filter
def getattr_field(obj, attr):
    return getattr(obj, attr, '')


@register.filter
def get_attr(obj, attr_name):
    """دسترسی امن به attribute مدل بدون recursion"""
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return ''  # اگر فیلد نبود، مقدار پیش‌فرض
    
    
@register.filter
def safe_attr(obj, attr):
    if obj is None:
        return ''
    return getattr(obj, attr, '')

@register.filter
def strval(value):
    return str(value)