from django import template

register = template.Library()

@register.filter
def include_value_in_item(value,item):
    """
    بررسی می‌کند آیا value داخل item وجود دارد یا نه
    item می‌تواند list / tuple / queryset / string باشد
    """
    if not item or not value:
        return False

    try:
        return value in item
    except TypeError:
        return False
    
@register.filter
def include_splited_0(value='',option=''):
    """
    بررسی می‌کند آیا value داخل item وجود دارد یا نه
    item می‌تواند list / tuple / queryset / string باشد
    """
    if not item or not value:
        return False
    r = option.split('-')[0]

    if not r:
        return False
    
    r = r.strip()
    
    try:
        return value in option
    except TypeError:
        return False