from .models import  AccessName, ApplicationValues,DepartmentValues
from ensaniapp_settings.models import EnsaniSettings
from ensani_soldires_management.access import battalion_and_groups_allowed,create_access_tree

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

    en = EnsaniSettings.objects.first()

    b,g = battalion_and_groups_allowed(request.user)
    nodes = create_access_tree(b,g)

    healthy_quick = []
    healthy_quick_options= [('healthy','سالم'),('moaf','معاف از رزم'),('grobe','گروه ب'),('grobe','نامشخص')]
    
    for q,title in healthy_quick_options:
        healthy_quick.append({
            'base_url':'soldiers_healthy_quick_export_excel',
            "q":f'physical_condition={q}',
            "title":title,
            "children": nodes,
        
        })

    quick_tree_items = [

        {
            "title": "خروجی اکسل سریع",
            'base_url':'soldiers_quick_export_excel',
            "children": nodes,
        },
        {
            "title": "وضعیت سلامت",
            'base_url':'soldiers_healthy_quick_export_excel',
            "children": healthy_quick,
        },
        
        {
            "title": "خروجی اکسل قبل سازماندهی",
            'class':'no-implment',
            "children": nodes,
        },
        {
            "title": "خروجی اکسل قبل بعد سازماندهی",
            'class':'no-implment',
            "children": nodes,
        },
        {
            "title": "چاپ فهرست سریع",
            'class':'no-implment',
            "children": nodes,
        },
    ]
    

    if permissions.get('dep').get('amoozesh'):
        kf_nodes = [
            {"title":"همه","q":"type=all"},
            {"title":"کفایت از بسیج","q":"type=basij"},
            {"title":"کفایت دار خدمت قبلی","q":"type=khedmat_ghabli"},
        ]
        quick_tree_items.append({
            "title": "کفایت دار",
            'base_url':'soldiers_kefayat_quick_export_excel',
            "children": kf_nodes,
        })
        quick_tree_items.append({
            "title": "چاپ کارنامه آموزش",
            'base_url':'soldiers_training_transcript_print',
            "children": nodes,
        })
    quick_tree=[
        {
            "title": "فهرست سریع",
            'base_url':'',
            "children": quick_tree_items,
        },
    ]
    return {
        'permissions': permissions,
        'en':en,
        'quick_tree':quick_tree,
        'quick_tree_base_url':'',
        'app':{
            'name':'سپهر',
            'version':'2.0.2',
            'title':'سامانه پذیرش هوشمند رزم آموز',
            'description':'',
        }
    }
