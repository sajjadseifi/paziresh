from ensaniapp_settings.models import EnsaniSettings
import zipfile, io, os, pandas as pd
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from soldiers.models import Soldier
from django.utils import timezone
from soldiers.constants import physical_condition_list ,Type_of_disease_list
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TestSalamatRavanForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.urls import reverse
from .access import get_user_battalions, get_user_battalion_groups,get_user_soldiers
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import TopSoldiersForm
from .access import get_user_soldiers


def get_battalion_group_context(request, soldiers_qs):
    battalions_allowed = get_user_battalions(request.user)
    groups_allowed = get_user_battalion_groups(request.user).select_related('gordan').order_by('name')

    selected_battalion = request.GET.get('battalion')
    if not selected_battalion and battalions_allowed.exists():
        selected_battalion = str(battalions_allowed.first().id)

    selected_group = request.GET.get('group')

    if groups_allowed.exists() and selected_battalion:
        valid_group = (
            groups_allowed
            .filter(id=int(selected_group), gordan_id=int(selected_battalion))
            .first()
            if selected_group else None
        )

        if valid_group:
            selected_group = str(valid_group.id)
        else:
            first_group_in_battalion = (
                groups_allowed
                .filter(gordan_id=int(selected_battalion))
                .first()
            )
            if first_group_in_battalion:
                selected_group = str(first_group_in_battalion.id)
            else:
                selected_group = str(groups_allowed.first().id)

    selected_battalion_obj = (
        battalions_allowed.filter(id=selected_battalion).first()
        if selected_battalion else None
    )

    selected_group_obj = (
        groups_allowed.filter(id=selected_group).first()
        if selected_group else None
    )

    # فیلتر سربازها
    en = EnsaniSettings.objects.first()
    soldiers = soldiers_qs

    if selected_group:
        ann = {'code_gorhan_int': Cast('code_gorhan', IntegerField())}

        if not en.tatbigh:
            kw = {'battalion_group': selected_group}
            order = ('code_gorhan_int',)
        else:
            ann['code_gorhan_nahai_int'] = Cast('code_gorhan_nahai', IntegerField())
            kw = {'t_battalion_group': selected_group}
            order = ('code_gorhan_nahai_int', 'code_gorhan_int')

        soldiers = (
            soldiers
            .annotate(**ann)
            .filter(**kw)
            .order_by(*order)
        )

    nodes = [{ 'title':'همه گردان ها', 'q':f'b=all' }]
    for b in battalions_allowed:
        children = [{ 'title':'همه گروهان ها', 'q':f'b={b.id}&g=all' }]
        for g in groups_allowed:
            if g.gordan.id == b.id:
                children.append({ 'title':f'گروهان {g.name}', 'q':f'g={g.id}' })
        
        nodes.append({ 'title':str(b),'q':f'b={b.id}','children': children })
        
    return {
        'soldiers': soldiers,
        'battalions': battalions_allowed,
        'groups': groups_allowed,
        'selected_battalion': selected_battalion,
        'selected_group': selected_group,
        'selected_battalion_name': selected_battalion_obj.name if selected_battalion_obj else None,
        'selected_group_name': selected_group_obj.name if selected_group_obj else None,
        'nodes':nodes,
    }


from django.db.models import IntegerField
from django.db.models.functions import Cast

def get_filtered_soldiers(soldiers_qs, battalion=None, group=None):
    """
    فیلتر و مرتب‌سازی سربازها بر اساس battalion و group با پشتیبانی از 'all'.
    مرتب‌سازی همواره بر اساس:
        گردان / گروهان / کد سازمانی

    :param soldiers_qs: QuerySet پایه Soldier
    :param battalion: id گردان، 'all' یا None
    :param group: id گروهان، 'all' یا None
    :return: QuerySet فیلتر شده و مرتب شده
    """
    # نرمال‌سازی ورودی‌ها: 'all' → None
    if battalion == 'all':
        battalion = None
    if group == 'all':
        group = None

    soldiers = soldiers_qs
    en = EnsaniSettings.objects.first()  # تنظیمات انسانی

    # Annotate برای مرتب‌سازی
    ann = {
        'code_gorhan_int': Cast('code_gorhan', IntegerField()),
        'current_code': Cast('code_gorhan', IntegerField()),
    }

    if en.tatbigh:
        ann['code_gorhan_nahai_int'] = Cast('code_gorhan_nahai', IntegerField())
        ann['current_code']=Cast('code_gorhan_nahai', IntegerField())
        order_fields = ['t_Gordan', 't_battalion_group', 'code_gorhan_nahai_int', 'code_gorhan_int']
    else:
        order_fields = ['Gordan', 'battalion_group', 'code_gorhan_int']

    soldiers = soldiers.annotate(**ann)

    # فیلتر گروه و گردان
    if group:
        if en.tatbigh:
            soldiers = soldiers.filter(t_battalion_group=group)
        else:
            soldiers = soldiers.filter(battalion_group=group)
    elif battalion:
        if en.tatbigh:
            soldiers = soldiers.filter(t_Gordan=battalion)
        else:
            soldiers = soldiers.filter(Gordan=battalion)

    # مرتب‌سازی نهایی
    soldiers = soldiers.order_by(*order_fields)

    return soldiers
