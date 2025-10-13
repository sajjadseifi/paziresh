from .models import UserAccess, AccessName, ApplicationValues

def user_access_context(request):
    """
    Context Processor:
    وضعیت دسترسی کاربر به بخش‌های مختلف برنامه (ApplicationValues)
    را در تمام صفحات به‌صورت lowercase فراهم می‌کند.
    خروجی نمونه:
    is_accesses = {
        'farmandehi': True/False,
        'niru_ensani': True/False,
        ...
    }
    """
    is_accesses = {}

    # مقداردهی اولیه (همه False)
    for app in ApplicationValues:
        is_accesses[app.name.lower()] = False

    # اگر کاربر لاگین کرده باشد
    if request.user.is_authenticated:
        user_accesses = request.user.accesses.filter(access_name=AccessName.APPLICATIONS.name)

        for access in user_accesses:
            if request.user.is_staff:
               is_accesses[access.access_value.lower()] = True
               continue
            is_access = access.access_value.lower() in [app.name.lower() for app in ApplicationValues]
            is_accesses[access.access_value.lower()] = is_access

    return {'is_accesses': is_accesses}
