from django import template
from accounts.models import AccessName  # مسیر را طبق پروژه خودت تنظیم کن
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.filter(access_name=key).first()

@register.filter
def ditem(dictionary, key):
    """دسترسی به مقدار یک دیکشنری با کلید"""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def filter_gordan(grohans, gordan_id):
    """
    گروهان‌ها را بر اساس gordan_id فیلتر می‌کند.
    usage: grohans|filter_gordan:g.id
    """
    return [gr for gr in grohans if gr.gordan_id == gordan_id]


@register.filter
def check_gorohan_access(user_access, grohan_id):
    """
    بررسی می‌کند که آیا کاربر به گروهان مشخص دسترسی دارد یا نه.
    user_access: queryset یا لیست UserAccess مربوط به کاربر
    grohan_id: id گروهان
    """
    if not user_access:
        return False

    # فقط دسترسی‌های GROHAN_SOLDIERS
    for access in user_access:
        if access.access_name == AccessName.GROHAN_SOLDIERS.name:
            # بررسی اینکه access_value برابر با id گروهان است
            try:
                if str(access.access_value) == str(grohan_id):
                    return True
            except Exception:
                continue
    return False


@register.filter
def check_application_access(user_access, application_section):
    """
    بررسی می‌کند که آیا کاربر به گروهان مشخص دسترسی دارد یا نه.
    user_access: queryset یا لیست UserAccess مربوط به کاربر
    grohan_id: id گروهان
    """
    if not user_access:
        return False

    # فقط دسترسی‌های GROHAN_SOLDIERS
    for access in user_access:
        if access.access_name == AccessName.APPLICATIONS.name:
            # بررسی اینکه access_value برابر با id گروهان است
            try:
                if str(access.access_value) == str(application_section):
                    return True
            except Exception:
                continue
    return False

@register.filter
def check_department_access(user_access, department_section):
    """
    بررسی می‌کند که آیا کاربر به یک واحد (department) خاص دسترسی دارد یا نه.
    user_access: queryset یا لیست UserAccess مربوط به کاربر
    department_section: نام یا کلید واحد مورد نظر (enum key)
    """
    if not user_access:
        return False

    # فقط دسترسی‌های مربوط به "DEPARTMENTS"
    for access in user_access:
        if access.access_name == AccessName.DEPARTMENTS.name:
            try:
                # بررسی اینکه access_value برابر کلید واحد است
                if str(access.access_value) == str(department_section):
                    return True
            except Exception:
                continue
    return False





