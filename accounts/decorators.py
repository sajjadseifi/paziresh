from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from accounts.context import user_access_context

def permissions_required(main_permission, fallback_permission=None, fallback_url=None, redirect_url='account_access_403'):
    """
    دکوراتوری مشابه login_required برای بررسی permissions
    - main_permission: 'dep.niru_ensani'
    - fallback_permission: 'dep.amoozesh'
    - fallback_url: لینک ریدایرکت در صورت داشتن fallback_permission
    - redirect_url: نام url برای صفحه 403
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # دریافت permissions از context processor یا request
            permissions = getattr(request, 'permissions', None) or request.context.get('permissions', None) if hasattr(request, 'context') else None

            if not permissions:
                # fallback: از user_access_context مستقیماً استفاده کن
                permissions = user_access_context(request)['permissions']

            def has_perm(perm_path):
                """
                بررسی وجود پرمیشن در دیکشنری تو در تو
                perm_path: 'dep.niru_ensani'
                """
                parts = perm_path.split('.')
                obj = permissions
                for part in parts:
                    if isinstance(obj, dict) and part in obj:
                        obj = obj[part]
                    else:
                        return False
                return bool(obj)

            # پرمیشن اصلی
            if has_perm(main_permission):
                return view_func(request, *args, **kwargs)

            # fallback
            if fallback_permission and has_perm(fallback_permission):
                if fallback_url:
                    return redirect(fallback_url)

            # اگر هیچکدام نبود => 403
            return redirect(reverse(redirect_url))

        return _wrapped_view
    return decorator

from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from accounts.context import user_access_context

def permissions_required_generic(
    allowed_permissions=None, 
    fallback_permissions=None, 
    access_denied_url='account_access_403'
):
    """
    دکوراتوری جنریک برای بررسی permissions
    - allowed_permissions: لیست پرمیشن‌هایی که اجازه دسترسی مستقیم دارند
        مثال: ['dep.amoozesh', 'dep.niru_ensani']
    - fallback_permissions: دیکشنری {permission_name: redirect_url}
        مثال: {'dep.gorohan': '/dashboard/gorohan/'}
    - access_denied_url: نام url برای صفحه دسترسی غیرمجاز
    """
    allowed_permissions = allowed_permissions or []
    fallback_permissions = fallback_permissions or {}

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # دریافت permissions
            permissions = getattr(request, 'permissions', None)
            if not permissions:
                permissions = user_access_context(request)['permissions']

            def has_perm(perm_path):
                """بررسی وجود پرمیشن در دیکشنری تو در تو"""
                parts = perm_path.split('.')
                obj = permissions
                for part in parts:
                    if isinstance(obj, dict) and part in obj:
                        obj = obj[part]
                    else:
                        return False
                return bool(obj)

            # بررسی allowed_permissions
            for perm in allowed_permissions:
                if has_perm(perm):
                    return view_func(request, *args, **kwargs)

            # بررسی fallback_permissions
            for perm, url in fallback_permissions.items():
                if has_perm(perm):
                    return redirect(url)

            # هیچکدام نبود => دسترسی غیرمجاز
            return redirect(reverse(access_denied_url))

        return _wrapped_view
    return decorator
