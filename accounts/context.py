from .models import UserAccess, AccessName, ApplicationValues,DepartmentValues
from ensaniapp_settings.models import EnsaniSettings

def user_access_context(request):
    """
    Context Processor:
    وضعیت دسترسی کاربر به بخش‌های مختلف برنامه (ApplicationValues)
    را در تمام صفحات به‌صورت lowercase فراهم می‌کند.
    خروجی نمونه:
    permissions = {
        'farmandehi': True/False,
        'niru_ensani': True/False,
        ...
    }
    """
    permissions = {
        'app':{},
        'dep':{},
    }

    # مقداردهی اولیه (همه False)
    for app in ApplicationValues:
        permissions['app'][app.name.lower()] = False

    # مقداردهی اولیه (همه False)
    for dep in DepartmentValues:
        permissions['dep'][dep.name.lower()] = False

    # اگر کاربر لاگین کرده باشد
    if request.user.is_authenticated:
        app_accesses = request.user.accesses.filter(access_name=AccessName.APPLICATIONS.name)
        dep_accesses = request.user.accesses.filter(access_name=AccessName.DEPARTMENTS.name)

        # حلقه برای enum ApplicationValues
        for app in ApplicationValues:
            key_access = app.name.lower()
            is_access = False

            if request.user.is_staff:
                is_access = True
            else:
                # بررسی اینکه آیا کاربر به این app دسترسی دارد
                is_access = app_accesses.filter(access_value__iexact=app.name).exists()

            permissions['app'][key_access] = is_access

        # حلقه برای enum DepartmentValues
        for dep in DepartmentValues:
            key_access = dep.name.lower()
            is_access = False

            if request.user.is_staff:
                is_access = True
            else:
                # بررسی اینکه آیا کاربر به این dep دسترسی دارد
                is_access = dep_accesses.filter(access_value__iexact=dep.name).exists()

            permissions['dep'][key_access] = is_access

    en = EnsaniSettings.objects.filter()
    return {'permissions': permissions,'en':en}
