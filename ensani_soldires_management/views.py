import jdatetime
import io
import zipfile
import pandas as pd
import openpyxl
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from ensani_soldires_management.forms import (
    FormUpdateGordan,
    Formjazbi,
    FormYegankhedmati,
    FormUpdateAllSoldiresHasbenAceptedInCourse,
    FormUpdateAllSoldires,
    FormRankGroup, FormAmirMahart
)
from soldiers.forms import FormUpdateRank, FormUpdateBank
from soldiers.models import Soldier
from ensani_letter.models import NormalLetterModels, CheckoutLetterModels
from battalions.models import battalion, battalion_group
from ensaniapp_settings.models import EnsaniSettings
from django.db import transaction
import logging
import xlwt

logger = logging.getLogger(__name__)
from django.http import HttpResponseServerError
from .constatns import *

from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.urls import reverse
from .access import get_user_battalions, get_user_battalion_groups,get_user_soldiers
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import TopSoldiersForm
from .access import get_user_soldiers

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory
from .forms import SoldierFilterForm, SoldierProblemForm, PROBLEM_FIELDS, PROBLEM_LABELS

from django.forms import formset_factory
from django.shortcuts import redirect, render
from .forms import SoldierProblemForm, SoldierFilterForm, PROBLEM_LABELS
import openpyxl
from django.http import HttpResponse
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from django.db import transaction
from django.shortcuts import redirect
from django.forms import formset_factory
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
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

from django.views.decorators.http import require_GET

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from soldiers.models import Soldier
from django.utils import timezone
from ensaniapp_settings.models import EnsaniSettings
import zipfile, io, os, pandas as pd
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.db.models import IntegerField,CharField
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from .forms import IdeologicalAssessmentBulkForm,BulkDynamicForm
from .utils import get_battalion_group_context,get_filtered_soldiers
from .models import SoldierTrainingRecord
from django.http import HttpResponse
from .models import Soldier
from .utils import get_filtered_soldiers
from core.excel import generate_excel
from django.http import HttpResponse
from .utils import get_filtered_soldiers
from ensaniapp_settings.models import EnsaniSettings
from django.shortcuts import render, redirect, get_object_or_404
from .models import IdeologicalAssessment
from .forms import IdeologicalAssessmentForm
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from accounts.context import user_access_context


def get_military_rank(education, score):
    """
    Determine military rank based on education level and score.
    
    Args:
        education (str): Education level of the soldier
        score (float): Score achieved by the soldier
        
    Returns:
        str: Military rank or error message
    """
    if education not in MILITARY_RANK_TABLE:
        return "مدرک تحصیلی نامعتبر است."

    for rank, (min_score, max_score) in MILITARY_RANK_TABLE[education].items():
        if min_score <= score <= max_score:
            return rank

    return "نمره در محدوده تعریف‌شده نیست."


# Utility functions
def clean_persian_text(text):
    """Replace Arabic characters with Persian equivalents and clean whitespace."""
    if text is None:
        return None
    return str(text).replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c", " ")


def get_excel_response(df, filename):
    """Create an Excel response with right-to-left formatting."""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')
        worksheet = writer.sheets['MyModelData']
        worksheet.sheet_view.rightToLeft = True

    return response


def process_excel_file(file, process_row_func):
    """Generic function to process Excel files."""
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active

    for row_idx in range(2, sheet.max_row + 1):
        row_data = []
        for col_idx in range(1, sheet.max_column + 1):
            cell_value = sheet.cell(row=row_idx, column=col_idx).value
            if cell_value is not None:
                cell_value = clean_persian_text(cell_value)
            row_data.append(cell_value)

        if row_data[0] is not None:  # Skip empty rows
            process_row_func(row_data)


def get_soldier_by_national_code(national_code):
    """Get soldier by national code with error handling."""
    return Soldier.objects.filter(National_Code=national_code).first()


@login_required
def all_soldire(request):
    soldires = Soldier.objects.filter(has_been_accepted=True, in_coures=True)
    context = {
        'results': soldires
    }

    return render(request, 'ensani_soldires_management/all_soldires.html', context)


@login_required
def soldier_search(request):
    query = request.GET.get('name')
    family = request.GET.get('family')
    national_code = request.GET.get('national_code')
    physical_condition = request.GET.get('physical_condition')
    marital_status = request.GET.get('marital_status')
    religion = request.GET.get('religion')
    acceptance_code = request.GET.get('acceptance_code')
    Grade = request.GET.get('Grade')
    Grade_precise = request.GET.get('Grade_precise')
    Gordan = request.GET.get('Gordan')
    amire = request.GET.get('amire')
    battaliongroup = request.GET.get('battaliongroup')
    admission_status = request.GET.get('admission_status')
    sort_by = request.GET.get('sort_by')
    soldiers = Soldier.objects.all().order_by('t_Gordan__name','t_battalion_group__name','code_gorhan_nahai')   
    gordan = battalion.objects.filter().all()
    grohan = battalion_group.objects.filter().all()
    count_f = soldiers
    if query:
        soldiers = soldiers.filter(name__icontains=query)
    if family:
        soldiers = soldiers.filter(family__icontains=family)
    if national_code:
        soldiers = soldiers.filter(National_Code__icontains=national_code)
    if physical_condition:
        soldiers = soldiers.filter(physical_condition__icontains=physical_condition)
    if marital_status:
        soldiers = soldiers.filter(marital_status=marital_status)
    if religion:
        soldiers = soldiers.filter(Religion__icontains=religion)
    if acceptance_code:
        soldiers = soldiers.filter(acceptance_code=acceptance_code)
    if Grade:
        soldiers = soldiers.filter(Grade=Grade)
    if Grade_precise:
        soldiers = soldiers.filter(Grade_precise=Grade_precise)

    if Gordan:
        soldiers = soldiers.filter(t_Gordan__name__icontains=Gordan)

    if battaliongroup:
        if Gordan is not None:
            soldiers = soldiers.filter(t_battalion_group__name__icontains=battaliongroup)

    if amire:
        soldiers = soldiers.filter(Amriye=amire)

    if admission_status:
        if admission_status == "accepted":
            soldiers = soldiers.filter(acceptance_code__isnull=False)  # پذیرش شده‌ها
        elif admission_status == "not_accepted":
            soldiers = soldiers.filter(acceptance_code__isnull=True)   # پذیرش نشده‌ها

    if sort_by:
        if sort_by == "final_group_code":
            soldiers = soldiers.order_by('t_Gordan__name','t_battalion_group__name','code_gorhan_nahai')  # کد نهایی گروهانی
        elif sort_by == "acceptance_code":
            soldiers = soldiers.order_by('acceptance_code')    # کد پذیرش
        elif sort_by == "group_code":
            soldiers = soldiers.order_by('code_gorhan')        # کد گروهانی
        elif sort_by == "full_name":
            soldiers = soldiers.order_by('name', 'family')    # نام و نام خانوادگی
        elif sort_by == "tallest":
            soldiers = soldiers.order_by('-height')           # بلندترین قد
        elif sort_by == "shortest":
            soldiers = soldiers.order_by('height')            # کوتاه‌ترین قد
        elif sort_by == "birth_date":
            soldiers = soldiers.order_by('birth_date')        # تاریخ تولد
    op_result = False
    count_e = soldiers
    if count_f != count_e:
        op_result = True

    context = {
        'results': soldiers, 'op_result': op_result, 'gordan': gordan, 'grohan': grohan,
    }

    return render(request, 'ensani_soldires_management/soldier_search.html', context)


def soldier_in_almahdi(request):
    units = [
        "آموزشگاه المهدی (عج) نزسا",
        "آموزشگاه المهدی (عج)",
        "(عج) المهدی آموزشگاه",
    ]

    soldiers = Soldier.objects.filter(unit_name__in=units)

    context = {
        'results': soldiers,
    }

    return render(request, 'ensani_soldires_management/soldier_list_almahdi.html', context)

@login_required
def get_grohan_by_gordan_for_search(request):
    gordan_name = request.GET.get('gordan_name')
    grohan_list = battalion_group.objects.filter(gordan__name__icontains=gordan_name).values('id', 'name')
    return JsonResponse(list(grohan_list), safe=False)


@login_required
def soldire_details(request, code):
    if request.method == "GET":
        soldire = Soldier.objects.filter(National_Code=code).first()
        normalLetter = NormalLetterModels.objects.filter(soldire=soldire).all()
        context = {'soldier': soldire, 'normalLetter': normalLetter, 'rank_mapping': RANK_MAPPING}
        return render(request, 'ensani_soldires_management/soldire_details.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ensani_letter.models import *
@login_required
def soldier_detail(request):
    code = request.GET.get('code') or request.POST.get('code')
    
    soldiers = Soldier.objects.all().order_by('name','family')
    

    if not code:
        # هیچ کدی در query string نیست
        return render(request, 'ensani_soldires_management/soldier_detail.html', {
            'code':code,
            'soldiers': soldiers,
            'soldier': None,
            'normalLetter': None,
            'rank_mapping': RANK_MAPPING,
            'message': "لطفاً ابتدا سرباز مورد نظر را انتخاب کنید."
        })

    soldier = Soldier.objects.filter(National_Code=code).first()

    if not soldier:
        # کد ملی اشتباه یا سرباز پیدا نشده
        return render(request, 'ensani_soldires_management/soldier_detail.html', {
            'code':code,
            'soldiers': soldiers,
            'soldier': None,
            'normalLetter': None,
            'rank_mapping': RANK_MAPPING,
            'message': "سربازی با این کد ملی یافت نشد. لطفاً دوباره تلاش کنید."
        })


    normalLetter = NormalLetterModels.objects.filter(soldire=soldier).all()
    rank_list = dict(RANK_MAPPING).keys()
    current_rank = soldier.rank
        
    rank_access = []
    if soldier.Grade == 'دکتری':
        rank_access=["ستوان یکم"]
    elif soldier.Grade == 'فوق لیسانس':
        rank_access=["ستوان سوم","ستوان دوم"]
    elif soldier.Grade == 'لیسانس':
        rank_access=["رزم‌آور سوم","رزم‌آور دوم","رزم‌آور یکم","رزمدار دوم","رزمدار یکم","ستوان سوم"]
    elif soldier.Grade == 'فوق دیپلم':
        rank_access=["رزم‌آور سوم","رزم‌آور دوم"]
    else:
        rank_access=["سرباز","سرباز دوم","سرباز یکم","رزمیار"]
    
    if request.method == "POST": 
        action = request.POST.get('action')
        print(action)
        if action == "rank":
            new_rank = request.POST.get('new_rank')
            if new_rank in rank_access and new_rank != soldier.rank:
                print(soldier.rank,new_rank)
                soldier.rank = new_rank
        if action == "IsUnit":
            # flag unit from user
            soldier.IsUnit = not soldier.IsUnit 
            
        soldier.save()

            
    # محاسبه تعداد انواع نامه‌ها
    letter_counts = {
        "training_inquiry": NormalLetterModels.objects.filter(soldire=soldier,subject ="استعلام کفایت از آموزش").count(),
        "normal": NormalLetterModels.objects.filter(soldire=soldier).count(),
        "checkout_before": NormalLetterModels.objects.filter(soldire=soldier,subject = "معرفی به کمیسیون شروع دوره آموزشی").count(),
        "checkout": CheckoutLetterModels.objects.filter(soldire=soldier).count(),
        "register": RegisterNormalLetter.objects.filter(normal_letter__soldire=soldier).count(),
        "runaway": RunawayNormallLetter.objects.filter(normal_letter__soldire=soldier).count(),
        "faraja": FarajaNormallLetter.objects.filter(normal_letter__soldire=soldier).count(),
        "moarefi": MoarefiNormallLetter.objects.filter(normal_letter__soldire=soldier).count(),
        "raw": RawLetter.objects.filter(soldier_national_code=code).count(),
    } 
    # my_letter.

    return render(request, 'ensani_soldires_management/soldier_detail.html', {
        'code':code,
        'soldiers': soldiers,
        'soldier': soldier,
        'rank_list':rank_list,
        'current_rank':current_rank,
        'rank_mapping': RANK_MAPPING,
        'normalLetter': normalLetter,
        'rank_access':rank_access,
        'letter_counts':letter_counts,
    })

@login_required
def export_to_excel_list_hazer_be_khdmat(request):
    """Export list of soldiers ready for service to Excel."""
    queryset = Soldier.objects.filter(
        has_been_accepted=True,
        willing_to_learn=True,
        in_coures=True
    ).values(
        'acceptance_code',
        'name',
        'family',
        'National_Code',
        't_Gordan__name',
        't_battalion_group__name',
        'code_gorhan_nahai'
    ).order_by('acceptance_code')

    df = pd.DataFrame(list(queryset))
    df.rename(columns={
        'acceptance_code': 'کد پذیرش',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'National_Code': 'کدملی',
        't_Gordan__name': 'نام گردان',
        't_battalion_group__name': 'نام گروهان',
        'code_gorhan_nahai': 'کد گروهان'
    }, inplace=True)

    return get_excel_response(df, 'list_hazer_be_khdmat')


@login_required
def export_to_excel_list_tajdid_dore(request):
    """Export list of soldiers ready for service to Excel."""
    sold = Soldier.objects.filter(has_been_accepted=True, IsCheckout=True).all()
    en = EnsaniSettings.objects.filter().first()
    data_list = []
    for s in sold:
        vazit = ""
        if s.has_been_accepted is True and s.IsCheckout is False and s.in_coures is True and s.willing_to_learn is True:
            vazit = "قبول"
        if s.has_been_accepted is True and s.IsCheckout is True:
            vazit = "مردود"
        check_out = ""
        check_out_date = ""
        hozor_time = en.tarihkepayanedore - en.tarikhpaziresh
        if s.IsCheckout is True:
            c = CheckoutLetterModels.objects.filter(soldire_id=s.id).first()
            if c is not None:
                check_out_date = c.create_time.date()
                hozor_time = (c.create_time.date() - en.tarikhpaziresh).days
            n = NormalLetterModels.objects.filter(subject="سازمان وظیفه عمومی فراجا", soldire_id=s.id).first()
            if s.the_medical_commission is True:
                check_out = "کمیسیون"
                vazit = "مردود"
            elif s.Sufficiency_of_mobilization is True:
                check_out = "کفایتی"
                hozor_time = ""
                vazit = ""
            elif s.Previous_service_record is True:
                check_out = "خدمت قبلی"
                hozor_time = ""
                vazit = ""
            elif n is not None:
                check_out = "سازمان وظیفه عمومی فراجا"
                vazit = ""
            else:
                check_out = "تجدید دوره"

        data_list.append(
            {
                "name": s.name,
                "family": s.family,
                "fathers_name": s.fathers_name,
                "National_Code": s.National_Code,
                "phone_number": s.phone_number,
                "home_phone_number": s.home_phone_number,
                "Relative_to_inclusive": s.Relative_to_inclusive,
                "Relative_to_inclusive_number": s.Relative_to_inclusive_number,
                "Date_of_dispatch": s.Date_of_dispatch,
                "Renewal_of_the_previous_period": s.Renewal_of_the_previous_period,
                "physical_condition": s.physical_condition,
                "check_out": check_out,
                "check_out_date": check_out_date,
            }
        )
    df = pd.DataFrame(list(data_list))

    df.rename(columns={
        'acceptance_code': 'کد پذیرش',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'National_Code': 'کدملی',
        'fathers_name': 'نام پدر',
        'phone_number': 'موبایل',
        'home_phone_number': 'خانه',
        'Relative_to_inclusive': 'بستگان',
        'Relative_to_inclusive_number': 'بستگان درجه یک',
        'Date_of_dispatch': 'تاریخ اعزام',
        'Renewal_of_the_previous_period': 'تجدید دوره از قبل',
        'physical_condition': 'وضعیت جسمانی',
        'check_out': 'تجدید دوره',
        'check_out_date': 'تاریخ تسویه حساب',

    }, inplace=True)

    return get_excel_response(df, 'list_tajdid_dore')


@login_required
def export_to_excel_list_sarbaz_tatbigh_nashode(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, in_coures=True, the_medical_commission=False,
                                      Previous_service_record=False, Sufficiency_of_mobilization=False,
                                      tatbigh=False, IsCheckout=False).values(
        'acceptance_code', 'name', 'family',
        'National_Code', 'Gordan__name', 'battalion_group__name', 't_Gordan__name', 't_battalion_group__name',
        'code_gorhan_nahai').order_by(
        'acceptance_code')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'acceptance_code': 'کد پذیرش',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'National_Code': 'کدملی',
        'Gordan__name': 'نام گردان',
        'battalion_group__name': 'نام گروهان',
        't_Gordan__name': 'نام گردان جدید',
        't_battalion_group__name': 'نام گروهان جدید',
        'code_gorhan_nahai': 'کد گروهان جدید'
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_tatbigh_nashode.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


class exel_update_gordan(LoginRequiredMixin, View):
    """View for updating soldier's battalion information from Excel."""
    template_name = 'ensani_soldires_management/update_gordan.html'

    def get(self, request):
        form = FormUpdateGordan()
        return render(request, self.template_name, {'form': form})

    def process_row(self, row_data):
        """Process a single row of Excel data."""
        if not row_data[0]:
            return

        soldier = get_soldier_by_national_code(row_data[0])
        if not soldier:
            return

        if row_data[5]:  # Battalion name exists
            t_gordan = battalion.objects.filter(name__icontains=row_data[5]).first()
            if t_gordan and row_data[6]:  # Group name exists
                t_gorohan = battalion_group.objects.filter(
                    gordan=t_gordan,
                    name__icontains=row_data[6]
                ).first()

                soldier.t_Gordan = t_gordan
                soldier.t_battalion_group = t_gorohan
                if row_data[7]:
                    soldier.code_gorhan_nahai = int(row_data[7])
                soldier.tatbigh = True
                soldier.save()

    def post(self, request):
        form = FormUpdateGordan(request.POST, request.FILES or None)
        if form.is_valid():
            process_excel_file(request.FILES['file'], self.process_row)
        return render(request, self.template_name, {'form': form})


class exel_jazbi(LoginRequiredMixin, View):
    def get(self, request):
        form = Formjazbi()
        form.fields['type'].choices = [("سپاه/مامور", 'سپاه/مامور'), ("نزسا", "نزسا"), ("موفق", "موفق")]
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_jazbi.html', cx)

    def post(self, request):
        form = Formjazbi(request.POST, request.FILES or None)
        form.fields['type'].choices = [("سپاه/مامور", 'سپاه/مامور'), ("نزسا", "نزسا"), ("موفق", "موفق")]
        cx = {'form': form}

        if form.is_valid():
            type = form.cleaned_data['type']
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و')
                    one_soldire_list.append(cell_value)
                if one_soldire_list[0] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if find_soldire is not None:
                        if type == "موفق":
                            find_soldire.Successful_recruitment = True
                            find_soldire.save()
                        else:
                            find_soldire.attraction_of_the_organization = type
                            find_soldire.save()

        return render(request, 'ensani_soldires_management/update_jazbi.html', cx)


@login_required
def export_to_excel_list_sarbvaz_test_salamat_ravan(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                      physical_condition="سالم", attraction_of_the_organization='هیچکدام').values(
        'acceptance_code', 'name', 'family',
        'National_Code', 't_Gordan__name', 't_battalion_group__name',
        'code_gorhan_nahai').order_by(
        't_Gordan__name', 't_battalion_group__name')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'National_Code': 'کدملی',
        'name': 'نام',
        'family': 'نام خانوادگی',
        't_Gordan__name': 'نام گردان جدید',
        't_battalion_group__name': 'نام گروهان جدید',
        'code_gorhan_nahai': 'کد گروهان جدید'
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_test_salamt_ravan.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


@login_required
def export_to_excel_list_sarbaz_be_sorat_gorohi(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'acceptance_code', 'name', 'family',
        'National_Code', 't_Gordan__name', 't_battalion_group__name',
        'code_gorhan_nahai').order_by(
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'acceptance_code': 'عدد پذیرش',
        'National_Code': 'کدملی',
        'name': 'نام',
        'family': 'نام خانوادگی',
        't_Gordan__name': 'نام گردان جدید',
        't_battalion_group__name': 'نام گروهان جدید',
        'code_gorhan_nahai': 'کد گروهان جدید'
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_goran_gorohani_codenahai.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


@login_required
def PrintPosheNokhodi(request):
    in_course_soldire = Soldier.objects.filter(in_coures=True, willing_to_learn=True).order_by('t_Gordan__name',
                                                                                               't_battalion_group__name',
                                                                                               'code_gorhan_nahai')   
    cx = {'soldires': in_course_soldire}
    return render(request, 'ensani_soldires_management/print_poshe_nokhodi.html', cx)


def clean_string(input_string):
    # جدا کردن رشته بر اساس "-"
    parts = input_string.split(" - ")

    # بررسی تعداد "-" در رشته
    if len(parts) > 2:
        # دوباره چسباندن اولین و دومین قسمت با "-"
        cleaned_string = " - ".join(parts[:2])
        return cleaned_string
    else:
        return input_string


class exel_yegaan_khedmat(LoginRequiredMixin, View):
    def get(self, request):
        form = FormYegankhedmati()
        form.fields['type'].choices = [(1, 'عادی'), (2, "امریه")]
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_yegann_khedmati.html', cx)

    def post(self, request):
        form = FormYegankhedmati(request.POST, request.FILES or None)
        form.fields['type'].choices = [(1, 'عادی'), (2, "امریه")]
        if not form.is_valid():
            cx = {'form': form}
            return render(request, 'ensani_soldires_management/update_yegann_khedmati.html', cx)
        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c",
                                                                                                              " ")
                    one_soldire_list.append(cell_value)
                if one_soldire_list[0] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if form.cleaned_data['type'] == "1":
                        if find_soldire is not None:
                            for iteam in LIST_YEGAN_BEKARGIRANDE:
                                i_c = clean_string(one_soldire_list[1])
                                i_c = i_c.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace(
                                    "\u200c",
                                    " ")
                                if iteam[1].replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace(
                                        "\u200c",
                                        " ") == i_c:
                                    find_soldire.yegan_name = one_soldire_list[1]
                                    find_soldire.unit_name = iteam[1]
                                    find_soldire.unit_type = iteam[2]
                                    find_soldire.unit_province = iteam[3]
                                    find_soldire.unit_address = iteam[4]
                                    find_soldire.IsUnit = True
                                    find_soldire.save()
                                    break
                    if form.cleaned_data['type'] == "2":
                        if find_soldire is not None:
                            for iteam in LIST_YEGAN_BEKARGIRANDE:
                                if iteam[1].replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace(
                                        "\u200c",
                                        " ") == one_soldire_list[1]:
                                    find_soldire.unit_name = iteam[1]
                                    find_soldire.unit_type = iteam[2]
                                    find_soldire.unit_province = iteam[3]
                                    find_soldire.unit_address = iteam[4]
                                    find_soldire.IsUnit = True
                            find_soldire.Amriye = True
                            find_soldire.Amriye_organization = one_soldire_list[1]
                            find_soldire.save()
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_yegann_khedmati.html', cx)


@login_required
def export_soldire_incoures_all_data(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'name', 'family', 'fathers_name', 'National_Code', 'acceptance_code', 't_Gordan__name',
        't_battalion_group__name', 'code_gorhan_nahai', 'Amriye', 'Amriye_organization', 'physical_condition',
        'Type_of_disease', 'Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
        'marital_status', 'Religion', 'Date_of_birth', 'place_of_birth', 'phone_number', 'home_phone_number',
        'Date_of_dispatch', 'province_name', 'city_name', 'Address', 'Place_of_Issue', 'height', 'Weight',
        'Renewal_of_the_previous_period', 'attraction_of_the_organization', 'unit_name', 'unit_type').order_by(
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عدد پذیرش',
        't_Gordan__name': 'نام گردان جدید',
        't_battalion_group__name': 'نام گروهان جدید',
        'code_gorhan_nahai': 'کد گروهان جدید',
        'Amriye': 'امریه دار',
        'Amriye_organization': 'سازمان امریه',
        'physical_condition': 'وضعیت جسمانی',
        'Type_of_disease': 'نوع بیماری',
        'Grade': 'مقطع تحصیلی',
        'Grade_precise': 'مقطع تحصیلی دقیق',
        'educational_level_of_the_system': 'مقطع تحصیلی سامانه',
        'Study_group': 'گروه تحصیلی',
        'marital_status': 'وضعیت تاهل',
        'Religion': 'مذهب',
        'Date_of_birth': 'تاریخ تولد',
        'place_of_birth': 'محل تولد',
        'phone_number': 'شماره موبایل',
        'home_phone_number': 'شماره منزل',
        'Date_of_dispatch': 'تاریخ اعزام',
        'province_name': 'نام استان',
        'city_name': 'نام شهر',
        'Address': 'آدرس',
        'Place_of_Issue': 'محل صدور',
        'height': 'قد',
        'Weight': 'وزن',
        'Renewal_of_the_previous_period': 'جدید دوره قبل',
        'attraction_of_the_organization': 'جذبی',
        'unit_name': 'نام یگان بکارگیرنده',
        'unit_type': 'نوع یگان بکارگیرنده',
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_all_soldire_in_course.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


@login_required
def export_soldire_Sufficiency_of_mobilization_all_data(request):
    queryset = Soldier.objects.filter(has_been_accepted=True,
                                      Sufficiency_of_mobilization=True).values(
        'name', 'family', 'fathers_name', 'National_Code', 'acceptance_code', 'Amriye', 'Amriye_organization',
        'physical_condition',
        'Type_of_disease', 'Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
        'marital_status', 'Religion', 'Date_of_birth', 'place_of_birth', 'phone_number', 'home_phone_number',
        'Date_of_dispatch', 'province_name', 'city_name', 'Address', 'Place_of_Issue', 'height', 'Weight',
        'Renewal_of_the_previous_period', 'attraction_of_the_organization', 'unit_name', 'unit_type').order_by(
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عدد پذیرش',
        'Amriye': 'امریه دار',
        'Amriye_organization': 'سازمان امریه',
        'physical_condition': 'وضعیت جسمانی',
        'Type_of_disease': 'نوع بیماری',
        'Grade': 'مقطع تحصیلی',
        'Grade_precise': 'مقطع تحصیلی دقیق',
        'educational_level_of_the_system': 'مقطع تحصیلی سامانه',
        'Study_group': 'گروه تحصیلی',
        'marital_status': 'وضعیت تاهل',
        'Religion': 'مذهب',
        'Date_of_birth': 'تاریخ تولد',
        'place_of_birth': 'محل تولد',
        'phone_number': 'شماره موبایل',
        'home_phone_number': 'شماره منزل',
        'Date_of_dispatch': 'تاریخ اعزام',
        'province_name': 'نام استان',
        'city_name': 'نام شهر',
        'Address': 'آدرس',
        'Place_of_Issue': 'محل صدور',
        'height': 'قد',
        'Weight': 'وزن',
        'Renewal_of_the_previous_period': 'جدید دوره قبل',
        'attraction_of_the_organization': 'جذبی',
        'unit_name': 'نام یگان بکارگیرنده',
        'unit_type': 'نوع یگان بکارگیرنده',
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_soldire_Sufficiency_of_mobilization_all_data.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


@login_required
def export_soldire_Previous_service_record_all_data(request):
    queryset = Soldier.objects.filter(has_been_accepted=True,
                                      Previous_service_record=True).values(
        'name', 'family', 'fathers_name', 'National_Code', 'acceptance_code', 'Amriye', 'Amriye_organization',
        'physical_condition',
        'Type_of_disease', 'Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
        'marital_status', 'Religion', 'Date_of_birth', 'place_of_birth', 'phone_number', 'home_phone_number',
        'Date_of_dispatch', 'province_name', 'city_name', 'Address', 'Place_of_Issue', 'height', 'Weight',
        'Renewal_of_the_previous_period', 'attraction_of_the_organization', 'unit_name', 'unit_type').order_by(
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عدد پذیرش',
        'Amriye': 'امریه دار',
        'Amriye_organization': 'سازمان امریه',
        'physical_condition': 'وضعیت جسمانی',
        'Type_of_disease': 'نوع بیماری',
        'Grade': 'مقطع تحصیلی',
        'Grade_precise': 'مقطع تحصیلی دقیق',
        'educational_level_of_the_system': 'مقطع تحصیلی سامانه',
        'Study_group': 'گروه تحصیلی',
        'marital_status': 'وضعیت تاهل',
        'Religion': 'مذهب',
        'Date_of_birth': 'تاریخ تولد',
        'place_of_birth': 'محل تولد',
        'phone_number': 'شماره موبایل',
        'home_phone_number': 'شماره منزل',
        'Date_of_dispatch': 'تاریخ اعزام',
        'province_name': 'نام استان',
        'city_name': 'نام شهر',
        'Address': 'آدرس',
        'Place_of_Issue': 'محل صدور',
        'height': 'قد',
        'Weight': 'وزن',
        'Renewal_of_the_previous_period': 'جدید دوره قبل',
        'attraction_of_the_organization': 'جذبی',
        'unit_name': 'نام یگان بکارگیرنده',
        'unit_type': 'نوع یگان بکارگیرنده',
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_soldire_Sufficiency_of_mobilization_all_data.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


class update_db_from_exel_all_soldire_in_course(LoginRequiredMixin, View):
    def get(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse()
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_db_from_exel_all_soldire_in_course.html', cx)

    def post(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request, 'ensani_soldires_management/update_db_from_exel_all_soldire_in_course.html', cx)
        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c",
                                                                                                              " ")
                    one_soldire_list.append(cell_value)
                if one_soldire_list[3] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[3]).first()
                    find_soldire.name = one_soldire_list[0]
                    find_soldire.family = one_soldire_list[1]
                    find_soldire.fathers_name = one_soldire_list[2]
                    find_soldire.acceptance_code = one_soldire_list[4]
                    if one_soldire_list[5] is not None:
                        gordan = battalion.objects.filter(name__icontains=one_soldire_list[5]).first()
                        find_soldire.t_Gordan = gordan
                        if one_soldire_list[6] is not None:
                            gorhan = battalion_group.objects.filter(name__icontains=one_soldire_list[6],
                                                                    gordan=gordan).first()
                            find_soldire.t_battalion_group = gorhan
                        if one_soldire_list[7] is not None:
                            find_soldire.code_gorhan_nahai = int(one_soldire_list[7])
                    find_soldire.Amriye = one_soldire_list[8]
                    find_soldire.Amriye_organization = one_soldire_list[9]
                    find_soldire.physical_condition = one_soldire_list[10]
                    find_soldire.Type_of_disease = one_soldire_list[11]
                    find_soldire.Grade = one_soldire_list[12]
                    find_soldire.Grade_precise = one_soldire_list[13]
                    find_soldire.educational_level_of_the_system = one_soldire_list[14]
                    find_soldire.Study_group = one_soldire_list[15]
                    find_soldire.marital_status = one_soldire_list[16]
                    find_soldire.Religion = one_soldire_list[17]
                    find_soldire.Date_of_birth = one_soldire_list[18]
                    find_soldire.Date_of_dispatch = one_soldire_list[19]
                    find_soldire.phone_number = one_soldire_list[20]
                    find_soldire.home_phone_number = one_soldire_list[21]
                    find_soldire.Date_of_dispatch = one_soldire_list[22]
                    find_soldire.province_name = one_soldire_list[23]
                    find_soldire.city_name = one_soldire_list[24]
                    find_soldire.Address = one_soldire_list[25]
                    find_soldire.Place_of_Issue = one_soldire_list[26]
                    find_soldire.height = one_soldire_list[27]
                    find_soldire.Weight = one_soldire_list[28]
                    find_soldire.Renewal_of_the_previous_period = one_soldire_list[29]
                    find_soldire.attraction_of_the_organization = one_soldire_list[30]
                    find_soldire.unit_name = one_soldire_list[31]
                    find_soldire.unit_type = one_soldire_list[32]
                    find_soldire.save()
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_yegann_khedmati.html', cx)


class update_db_from_exel_all_soldire_Previous_service_record(LoginRequiredMixin, View):
    def get(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/update_db_from_exel_all_soldire_Previous_service_record.html', cx)

    def post(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'ensani_soldires_management/update_db_from_exel_all_soldire_Previous_service_record.html', cx)
        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c",
                                                                                                              " ")
                    one_soldire_list.append(cell_value)
                if one_soldire_list[3] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[3]).first()
                    find_soldire.name = one_soldire_list[0]
                    find_soldire.family = one_soldire_list[1]
                    find_soldire.fathers_name = one_soldire_list[2]
                    find_soldire.acceptance_code = one_soldire_list[4]
                    find_soldire.Amriye = one_soldire_list[5]
                    find_soldire.Amriye_organization = one_soldire_list[6]
                    find_soldire.physical_condition = one_soldire_list[7]
                    find_soldire.Type_of_disease = one_soldire_list[8]
                    find_soldire.Grade = one_soldire_list[9]
                    find_soldire.educational_level_of_the_system = one_soldire_list[10]
                    find_soldire.Grade = one_soldire_list[11]
                    find_soldire.Study_group = one_soldire_list[12]
                    find_soldire.marital_status = one_soldire_list[13]
                    find_soldire.Religion = one_soldire_list[14]
                    find_soldire.Date_of_birth = one_soldire_list[15]
                    find_soldire.place_of_birth = one_soldire_list[16]
                    find_soldire.phone_number = one_soldire_list[17]
                    find_soldire.home_phone_number = one_soldire_list[18]
                    find_soldire.Date_of_dispatch = one_soldire_list[19]
                    find_soldire.province_name = one_soldire_list[20]
                    find_soldire.city_name = one_soldire_list[21]
                    find_soldire.Address = one_soldire_list[22]
                    find_soldire.Date_of_dispatch = one_soldire_list[23]
                    find_soldire.height = one_soldire_list[24]
                    find_soldire.Weight = one_soldire_list[25]
                    find_soldire.Renewal_of_the_previous_period = one_soldire_list[26]
                    find_soldire.attraction_of_the_organization = one_soldire_list[27]
                    find_soldire.unit_name = one_soldire_list[28]
                    find_soldire.unit_type = one_soldire_list[29]
                    find_soldire.save()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/update_db_from_exel_all_soldire_Previous_service_record.html', cx)


class update_db_from_exel_all_soldire_Sufficiency_of_mobilization(LoginRequiredMixin, View):
    def get(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/update_db_from_exel_all_soldire_Sufficiency_of_mobilization.html', cx)

    def post(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'ensani_soldires_management/update_db_from_exel_all_soldire_Sufficiency_of_mobilization.html',
                          cx)

        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c",
                                                                                                              " ")
                    one_soldire_list.append(cell_value)
                if one_soldire_list[3] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[3]).first()
                    find_soldire.name = one_soldire_list[0]
                    find_soldire.family = one_soldire_list[1]
                    find_soldire.fathers_name = one_soldire_list[2]
                    find_soldire.acceptance_code = one_soldire_list[4]
                    find_soldire.Amriye = one_soldire_list[5]
                    find_soldire.Amriye_organization = one_soldire_list[6]
                    find_soldire.physical_condition = one_soldire_list[7]
                    find_soldire.Type_of_disease = one_soldire_list[8]
                    find_soldire.Grade = one_soldire_list[9]
                    find_soldire.educational_level_of_the_system = one_soldire_list[10]
                    find_soldire.Grade = one_soldire_list[11]
                    find_soldire.Study_group = one_soldire_list[12]
                    find_soldire.marital_status = one_soldire_list[13]
                    find_soldire.Religion = one_soldire_list[14]
                    find_soldire.Date_of_birth = one_soldire_list[15]
                    find_soldire.place_of_birth = one_soldire_list[16]
                    find_soldire.phone_number = one_soldire_list[17]
                    find_soldire.home_phone_number = one_soldire_list[18]
                    find_soldire.Date_of_dispatch = one_soldire_list[19]
                    find_soldire.province_name = one_soldire_list[20]
                    find_soldire.city_name = one_soldire_list[21]
                    find_soldire.Address = one_soldire_list[22]
                    find_soldire.Date_of_dispatch = one_soldire_list[23]
                    find_soldire.height = one_soldire_list[24]
                    find_soldire.Weight = one_soldire_list[25]
                    find_soldire.Renewal_of_the_previous_period = one_soldire_list[26]
                    find_soldire.attraction_of_the_organization = one_soldire_list[27]
                    find_soldire.unit_name = one_soldire_list[28]
                    find_soldire.unit_type = one_soldire_list[29]
                    find_soldire.save()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/update_db_from_exel_all_soldire_Sufficiency_of_mobilization.html', cx)


@login_required
def import_and_export_excel_maharat(request):
    if request.method == 'POST':
        form = FormAmirMahart(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']

            try:
                national_codes_df = pd.read_excel(excel_file)
                national_codes = national_codes_df['National_Code'].tolist()
            except Exception as e:
                return HttpResponse("خطا در خواندن فایل اکسل: " + str(e))

            soldiers_data = []
            for code in national_codes:
                soldier = Soldier.objects.filter(
                    National_Code__icontains=code
                ).values('National_Code', 'Date_of_birth', 'Address', 'home_phone_number', 'phone_number', 'Grade',
                         'name', 'family', 'fathers_name').first()
                if soldier:
                    soldiers_data.append(soldier)

            df = pd.DataFrame(soldiers_data)
            df.rename(columns={
                'fathers_name': 'نام پدر',
                'family': 'نام خانوادگی',
                'name': 'نام',
                'Grade': 'مدرک تحصیلی',
                'phone_number': 'شماره موبایل',
                'home_phone_number': 'منزل',
                'Address': 'آدرس',
                'Date_of_birth': 'تاریخ تولد',
                'National_Code': 'کدملی',
            }, inplace=True)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=soldiers_filtered_data.xlsx'

            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Filtered Soldiers Data')

            return response
    else:
        form = FormAmirMahart()

    return render(request, 'ensani_soldires_management/import_export_maharat.html', {'form': form})

import io
import zipfile
import xlwt
import pandas as pd
from django.http import HttpResponse
from ensani.excel_utils import sakhtar_kafiat_to_excel_bytes,sakhtar_kafiat_to_excel_xls_bytes
@login_required
def import_and_export_multiple_excel_sakhtar_sazi(request):
    # ایجاد فایل فشرده در حافظه
    zip_buffer = io.BytesIO()

    # باز کردن فایل فشرده برای نوشتن فایل‌ها
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # مجموعه‌های مختلف داده‌ها برای ایجاد فایل‌های مختلف اکسل
        data_sets = {}

        bn = battalion.objects.all()
        for b in bn:
            for bg in battalion_group.objects.filter(gordan=b):
                # تعریف مجموعه داده برای هر گروهان
                soldiers_filtered_data = Soldier.objects.filter(
                    t_battalion_group=bg,
                    t_Gordan=b,
                    willing_to_learn=True,
                    in_coures=True
                ).order_by('code_gorhan_nahai').values(
                    'National_Code', 'code_gorhan_nahai'
                )

                # اضافه کردن مجموعه داده به دیکشنری
                data_sets[f"{b.name}_{bg.name}"] = soldiers_filtered_data

        # ایجاد هر فایل اکسل و اضافه کردن به فایل ZIP
        for file_name, queryset in data_sets.items():
            # تبدیل queryset به DataFrame
            df = pd.DataFrame(list(queryset))

            if not df.empty:  # بررسی خالی نبودن مجموعه داده
                # تغییر نام ستون‌ها
                df.rename(columns={
                    'National_Code': 'کد ملی',
                    'code_gorhan_nahai': 'کد سازمانی'
                }, inplace=True)

                excel_buffer = io.BytesIO()
                # نوشتن DataFrame در فایل اکسل
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)

                # افزودن فایل اکسل به فایل فشرده
                zf.writestr(f'{file_name}.xlsx', excel_buffer.getvalue())

        excel_bytes = sakhtar_kafiat_to_excel_bytes()
        zf.writestr(f'کفایتی.xlsx', excel_bytes.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="sakhtar_sazi.zip"'
    return response


@login_required
def import_and_export_multiple_excel_sakhtar_sazi_xls(request):
    # ایجاد فایل فشرده در حافظه
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zf:
        data_sets = {}

        bn = battalion.objects.all()
        for b in bn:
            for bg in battalion_group.objects.filter(gordan=b):
                soldiers_filtered_data = Soldier.objects.filter(
                    t_battalion_group=bg,
                    t_Gordan=b,
                    willing_to_learn=True,
                    in_coures=True
                ).order_by('code_gorhan_nahai').values(
                    'National_Code', 'code_gorhan_nahai'
                )
                data_sets[f"{b.name}_{bg.name}"] = soldiers_filtered_data

        for file_name, queryset in data_sets.items():
            df = pd.DataFrame(list(queryset))
            if not df.empty:
                df.rename(columns={
                    'National_Code': 'کد ملی',
                    'code_gorhan_nahai': 'کد سازمانی'
                }, inplace=True)

                excel_buffer = io.BytesIO()
                wb = xlwt.Workbook()
                ws = wb.add_sheet("فهرست-فراگیران")

                # نوشتن هدر
                for col_idx, col_name in enumerate(df.columns):
                    ws.write(0, col_idx, col_name)

                # نوشتن داده‌ها
                for row_idx, row in enumerate(df.itertuples(index=False), start=1):
                    for col_idx, value in enumerate(row):
                        ws.write(row_idx, col_idx, value)

                wb.save(excel_buffer)
                zf.writestr(f"{file_name}.xls", excel_buffer.getvalue())

        # کفایتی هم می‌توان به همان صورت اضافه کرد
        excel_bytes = sakhtar_kafiat_to_excel_xls_bytes()  # این فایل هنوز xlsx است
        zf.writestr(f'کفایتی.xls', excel_bytes.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="sakhtar_sazi_xls.zip"'
    return response

@login_required
def export_to_excel_list_not_accepted(request):
    queryset = Soldier.objects.filter(has_been_accepted=False, date_improt_type='سامانه').values(
        'name', 'family', 'fathers_name',
        'National_Code', 'phone_number', 'home_phone_number')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'phone_number': 'موبایل',
        'home_phone_number': 'منزل',

    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export_to_excel_list_not_accepted.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


def calculate_score():
    """Calculate scores for all eligible soldiers."""

    # Score mapping constants
    DISCIPLINE_SCORES = {13: 0.5, 14: 0.5, 15: 1, 16: 1, 17: 1.5, 18: 1.5, 19: 2, 20: 2}
    BATTALION_ACTIVITY_SCORES = {16: 0.5, 17: 1, 18: 1.5, 19: 2, 20: 2.5}
    BATTALION_SAMPLE_SCORE = 2
    BASIJ_EFFICIENCY_SCORES = {'30 روزه': 0.5, '45 روزه': 1}
    IDEOLOGICAL_SCORES = {18: 0.4, 19: 0.7, 20: 1}
    TOP_THREE_SCORES = {'نفر اول': 2, 'نفر دوم': 1.5, 'نفر سوم': 1}

    def get_shooting_score(score):
        """Calculate shooting score based on ranges."""
        if 80 <= score < 85:
            return 0.4
        elif 85 <= score < 90:
            return 0.7
        elif 90 <= score < 95:
            return 1.5
        elif 95 <= score <= 100:
            return 2
        return 0

    def get_award_score(count, scores):
        """Calculate award score based on count and score mapping."""
        if count <= 0:
            return 0
        elif count > 3:
            return max(scores.values())
        return scores.get(count, 0)

    AWARD_SCORES = {
        'global': {1: 0.3, 2: 0.4},
        'national': {1: 0.2, 2: 0.3},
        'provincial': {1: 0.1, 2: 0.2}
    }

    ARTICLE_SCORES = {
        'global': {1: 0.2, 2: 0.3},
        'publications': {1: 0.2, 2: 0.3}
    }

    soldiers = Soldier.objects.filter(
        has_been_accepted=True,
        willing_to_learn=True,
        in_coures=True
    )

    for soldier in soldiers:
        total = 0

        # Battalion scores
        total += DISCIPLINE_SCORES.get(int(soldier.discipline_score), 0)
        total += BATTALION_ACTIVITY_SCORES.get(int(soldier.battalion_activity), 0)
        total += BATTALION_SAMPLE_SCORE if soldier.battalion_sample else 0

        # Basij scores
        total += float(soldier.basij_experience) * 0.0142857  # Active Basij experience
        total += float(soldier.council_experience) * 0.01  # Council experience
        total += BASIJ_EFFICIENCY_SCORES.get(str(soldier.basij_efficiency), 0)

        # Ideological and training scores
        total += IDEOLOGICAL_SCORES.get(int(soldier.ideological_score), 0)
        total += get_shooting_score(int(soldier.shooting_score))
        total += TOP_THREE_SCORES.get(soldier.top_three, 0)

        # Personal achievements
        total += soldier.quran_memorization * 0.1  # Quran memorization
        total += 1 if soldier.nahj_memorization else 0  # Nahj memorization
        total += 1 if soldier.sajjadiya_memorization else 0  # Sajjadiya memorization

        # Awards and publications
        total += get_award_score(soldier.global_awards, AWARD_SCORES['global'])
        total += get_award_score(soldier.national_awards, AWARD_SCORES['national'])
        total += get_award_score(soldier.provincial_awards, AWARD_SCORES['provincial'])
        total += get_award_score(soldier.global_articles, ARTICLE_SCORES['global'])
        total += get_award_score(soldier.publications, ARTICLE_SCORES['publications'])

        # Cap total score at 20
        total = min(total, 20)

        # Determine rank
        if soldier.Amriye or soldier.physical_condition != 'سالم':
            rank = get_military_rank(soldier.Grade, 0)
        else:
            rank = get_military_rank(soldier.Grade, total)

        # Update soldier
        soldier.rank = rank
        soldier.total_score = total
        soldier.save()


def calculate_score_for_soldiers(soldiers):
    """Calculate scores for all eligible soldiers."""

    # Score mapping constants
    DISCIPLINE_SCORES = {13: 0.5, 14: 0.5, 15: 1, 16: 1, 17: 1.5, 18: 1.5, 19: 2, 20: 2}
    BATTALION_ACTIVITY_SCORES = {16: 0.5, 17: 1, 18: 1.5, 19: 2, 20: 2.5}
    BATTALION_SAMPLE_SCORE = 2
    BASIJ_EFFICIENCY_SCORES = {'30 روزه': 0.5, '45 روزه': 1}
    IDEOLOGICAL_SCORES = {18: 0.4, 19: 0.7, 20: 1}
    TOP_THREE_SCORES = {'نفر اول': 2, 'نفر دوم': 1.5, 'نفر سوم': 1}

    def get_shooting_score(score):
        """Calculate shooting score based on ranges."""
        if 80 <= score < 85:
            return 0.4
        elif 85 <= score < 90:
            return 0.7
        elif 90 <= score < 95:
            return 1.5
        elif 95 <= score <= 100:
            return 2
        return 0

    def get_award_score(count, scores):
        """Calculate award score based on count and score mapping."""
        if count <= 0:
            return 0
        elif count > 3:
            return max(scores.values())
        return scores.get(count, 0)

    AWARD_SCORES = {
        'global': {1: 0.3, 2: 0.4},
        'national': {1: 0.2, 2: 0.3},
        'provincial': {1: 0.1, 2: 0.2}
    }

    ARTICLE_SCORES = {
        'global': {1: 0.2, 2: 0.3},
        'publications': {1: 0.2, 2: 0.3}
    }

    for soldier in soldiers:
        total = 0

        # Battalion scores
        total += DISCIPLINE_SCORES.get(int(soldier.discipline_score), 0)
        total += BATTALION_ACTIVITY_SCORES.get(int(soldier.battalion_activity), 0)
        total += BATTALION_SAMPLE_SCORE if soldier.battalion_sample else 0

        # Basij scores
        total += float(soldier.basij_experience) * 0.0142857  # Active Basij experience
        total += float(soldier.council_experience) * 0.01  # Council experience
        total += BASIJ_EFFICIENCY_SCORES.get(str(soldier.basij_efficiency), 0)

        # Ideological and training scores
        total += IDEOLOGICAL_SCORES.get(int(soldier.ideological_score), 0)
        total += get_shooting_score(int(soldier.shooting_score))
        total += TOP_THREE_SCORES.get(soldier.top_three, 0)

        # Personal achievements
        total += soldier.quran_memorization * 0.1  # Quran memorization
        total += 1 if soldier.nahj_memorization else 0  # Nahj memorization
        total += 1 if soldier.sajjadiya_memorization else 0  # Sajjadiya memorization

        # Awards and publications
        total += get_award_score(soldier.global_awards, AWARD_SCORES['global'])
        total += get_award_score(soldier.national_awards, AWARD_SCORES['national'])
        total += get_award_score(soldier.provincial_awards, AWARD_SCORES['provincial'])
        total += get_award_score(soldier.global_articles, ARTICLE_SCORES['global'])
        total += get_award_score(soldier.publications, ARTICLE_SCORES['publications'])

        # Cap total score at 20
        total = min(total, 20)

        # Determine rank
        if soldier.Amriye or soldier.physical_condition != 'سالم':
            rank = get_military_rank(soldier.Grade, 0)
        else:
            rank = get_military_rank(soldier.Grade, total)

        # Update soldier
        soldier.rank = rank
        soldier.total_score = total
        soldier.save()



class import_rank_from_exel(LoginRequiredMixin, View):
    def get(self, request):
        form = FormUpdateRank()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/import_rank_from_exel.html', cx)

    def post(self, request):
        form = FormUpdateRank(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'ensani_soldires_management/import_rank_from_exel.html',
                          cx)

        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    one_soldire_list.append(cell_value)

                if one_soldire_list[0] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if find_soldire is not None:
                        if one_soldire_list[6] is not None:
                            find_soldire.discipline_score = float(one_soldire_list[6])
                        else:
                            find_soldire.discipline_score = 0
                        if one_soldire_list[7] is not None:
                            find_soldire.basij_experience = float(one_soldire_list[7])
                        else:
                            find_soldire.basij_experience = 0

                        if one_soldire_list[8] is not None:
                            find_soldire.council_experience = float(one_soldire_list[8])
                        else:
                            find_soldire.council_experience = 0

                        if one_soldire_list[9] is not None:
                            find_soldire.ideological_score = float(one_soldire_list[9])
                        else:
                            find_soldire.ideological_score = 0

                        find_soldire.shooting_score = one_soldire_list[10] or 0
                        find_soldire.global_awards = one_soldire_list[11] or 0
                        find_soldire.national_awards = one_soldire_list[12] or 0
                        find_soldire.provincial_awards = one_soldire_list[13] or 0
                        find_soldire.global_articles = one_soldire_list[14] or 0
                        find_soldire.publications = one_soldire_list[15] or 0
                        find_soldire.battalion_activity = one_soldire_list[16]
                        find_soldire.battalion_sample = one_soldire_list[17] or False
                        find_soldire.basij_efficiency = one_soldire_list[18] or 0
                        find_soldire.top_three = one_soldire_list[19] or 0
                        find_soldire.quran_memorization = one_soldire_list[20] or 0
                        find_soldire.nahj_memorization = one_soldire_list[21] or False
                        find_soldire.sajjadiya_memorization = one_soldire_list[22] or False
                        find_soldire.save()

        cx = {'form': form}
        calculate_score()
        return render(request,
                      'ensani_soldires_management/import_rank_from_exel.html', cx)


@login_required
def export_to_excel_list_bank(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'name', 'family', 'fathers_name',
        'National_Code', 'acceptance_code', 't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai',
        'bank_number', 'province_name', 'city_name').order_by('t_Gordan',
                                                              't_battalion_group',
                                                              'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عددپذیرش',
        't_Gordan__name': 'گردان',
        't_battalion_group__name': 'گروهان',
        'code_gorhan_nahai': 'کدسازمانی',
        'province_name': 'استان',
        'city_name': 'شهر',
        'bank_number': 'شماره حساب',

    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export_to_excel_list_bank_number.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


#
# class import_bank_number_from_exel(LoginRequiredMixin, View):
#     def get(self, request):
#         form = FormUpdateBank()
#         cx = {'form': form}
#         return render(request,
#                       'ensani_soldires_management/import_bank_from_exel.html', cx)
#
#     def post(self, request):
#         form = FormUpdateBank(request.POST, request.FILES or None)
#         if not form.is_valid():
#             cx = {'form': form}
#             return render(request,
#                           'ensani_soldires_management/import_bank_from_exel.html',
#                           cx)
#
#         else:
#             exel = request.FILES['file']
#
#             workbook = openpyxl.load_workbook(exel)
#
#             # انتخاب شیت اول
#             sheet = workbook.active
#
#             # بدست آوردن تعداد ردیف‌ها و ستون‌ها
#             num_rows = sheet.max_row
#             num_cols = sheet.max_column
#
#             # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
#             for row_idx in range(2, num_rows + 1):
#                 one_soldire_list = []
#                 for col_idx in range(1, num_cols + 1):
#                     # مقدار سلول را بخوانید
#                     cell_value = sheet.cell(row=row_idx, column=col_idx).value
#                     one_soldire_list.append(cell_value)
#                 if one_soldire_list[0] is not None:
#                     find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
#                     if find_soldire is not None:
#                         find_soldire.bank_number = one_soldire_list[1]
#                         find_soldire.save()
#         cx = {'form': form}
#         calculate_score()
#         return render(request,
#                       'ensani_soldires_management/import_bank_from_exel.html', cx)


class import_bank_number_from_exel(LoginRequiredMixin, View):
    def get(self, request):
        form = FormUpdateBank()
        return render(request, 'ensani_soldires_management/import_bank_from_exel.html', {'form': form})

    def post(self, request):
        form = FormUpdateBank(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'ensani_soldires_management/import_bank_from_exel.html', {'form': form})

        try:
            excel_file = request.FILES['file']
            # استفاده از حالت خواندن بهینه
            workbook = openpyxl.load_workbook(excel_file, read_only=True)
            sheet = workbook.active

            soldiers_to_update = []
            # استفاده از iter_rows برای خواندن بهینه‌ی ردیف‌ها
            for row in sheet.iter_rows(min_row=2, values_only=True):
                national_code = row[0]
                bank_number = row[1]
                if national_code is not None:
                    soldier = Soldier.objects.filter(National_Code=national_code).first()
                    if soldier:
                        soldier.bank_number = bank_number
                        soldiers_to_update.append(soldier)

            # به‌روزرسانی دسته‌ای برای کاهش تعداد فراخوانی‌های دیتابیس
            if soldiers_to_update:
                with transaction.atomic():
                    Soldier.objects.bulk_update(soldiers_to_update, ['bank_number'])

            calculate_score()

        except Exception as e:
            logger.exception("Error processing Excel file")
            return HttpResponseServerError("An error occurred while processing the file.")

        return render(request, 'ensani_soldires_management/import_bank_from_exel.html', {'form': form})


@login_required
def rank_group_print(request):
    if request.method == "GET":
        form = FormRankGroup()

        context = {
            'form': form,
        }
        return render(request, 'ensani_soldires_management/rank_selector.html', context)
    if request.method == "POST":
        form = FormRankGroup(request.POST, request.FILES or None)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'ensani_soldires_management/rank_selector.html', context)
        start = int(form.cleaned_data['start']) + 1
        end = int(form.cleaned_data['end']) + 1

        sarbazha = Soldier.objects.filter(in_coures=True,
                                          has_been_accepted=True, willing_to_learn=True, acceptance_code__gte=start,
                                          acceptance_code__lt=end).order_by(
            'acceptance_code').all()
        en = EnsaniSettings.objects.filter().first()
        time = jdatetime.datetime.now()
        context = {
            'sarbazha': sarbazha,
            'en': en,
            'time': time,
        }
        return render(request, 'ensani_soldires_management/rank_print.html', context)


@login_required
def rank_group_print_gordani(request):
    sarbazha = Soldier.objects.filter(in_coures=True,
                                      has_been_accepted=True, willing_to_learn=True,
                                      ).all().order_by(
        't_Gordan', 't_battalion_group', 'code_gorhan_nahai').all()
    en = EnsaniSettings.objects.filter().first()
    time = jdatetime.datetime.now()

    context = {
        'sarbazha': sarbazha,
        'en': en,
        'time': time,
    }
    return render(request, 'ensani_soldires_management/rank_print.html', context)

from django.db.models import Case, When, Value, IntegerField

@login_required
def export_to_excel_list_rank(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'name', 'family', 'fathers_name',
        'National_Code', 'acceptance_code', 't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai',
        'rank').order_by('t_Gordan',
                         't_battalion_group',
                         'code_gorhan_nahai')

    rank_cases = [
        When(rank=rank_name, then=Value(rank_code)) 
        for rank_name, rank_code in RANK_MAPPING.items()
    ]

    queryset = queryset.annotate(rank_code=Case(
        *rank_cases,
        output_field=IntegerField()
    ))
    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عددپذیرش',
        't_Gordan__name': 'گردان',
        't_battalion_group__name': 'گروهان',
        'code_gorhan_nahai': 'کدسازمانی',
        'rank': 'درجه',
        'rank_code': 'کد درجه',

    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export_to_excel_list_rank.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


@login_required
def export_to_excel_list_goili(request):
    # queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
    #     'name', 'family', 'fathers_name',
    #     'National_Code', 'Grade', 'Study_group', 'Date_of_dispatch', 'attraction_of_the_organization',
    #     'Renewal_of_the_previous_period', 'physical_condition',
    #     'code_gorhan_nahai',
    #     'rank').order_by('t_Gordan',
    #                      't_battalion_group',
    #                      'code_gorhan_nahai')
    #
    sold = Soldier.objects.filter(has_been_accepted=True).all()
    en = EnsaniSettings.objects.filter().first()
    data_list = []
    for s in sold:
        vazit = ""
        if s.has_been_accepted is True and s.IsCheckout is False and s.in_coures is True and s.willing_to_learn is True:
            vazit = "قبول"
        if s.has_been_accepted is True and s.IsCheckout is True:
            vazit = "مردود"
        check_out = ""
        check_out_date = ""
        hozor_time = en.tarihkepayanedore - en.tarikhpaziresh
        if s.IsCheckout is True:
            c = CheckoutLetterModels.objects.filter(soldire_id=s.id).first()
            if c is not None:
                check_out_date = c.create_time.date()
                hozor_time = (c.create_time.date() - en.tarikhpaziresh).days
            n = NormalLetterModels.objects.filter(subject="سازمان وظیفه عمومی فراجا", soldire_id=s.id).first()
            if s.the_medical_commission is True:
                check_out = "کمیسیون"
                vazit = "مردود"
            elif s.Sufficiency_of_mobilization is True:
                check_out = "کفایتی"
                hozor_time = ""
                vazit = ""
            elif s.Previous_service_record is True:
                check_out = "خدمت قبلی"
                hozor_time = ""
                vazit = ""
            elif n is not None:
                check_out = "سازمان وظیفه عمومی فراجا"
                vazit = ""
            else:
                check_out = "تجدید دوره"

        data_list.append(
            {
                "name": s.name,
                "family": s.family,
                "fathers_name": s.fathers_name,
                "National_Code": s.National_Code,
                "Grade": s.Grade,
                "Study_group": s.Study_group,
                "Date_of_dispatch": s.Date_of_dispatch,
                "shomare_sore": en.shomare_dore,
                "yegan_ezam": "المهدی",
                "attraction_of_the_organization": s.attraction_of_the_organization,
                "Renewal_of_the_previous_period": s.Renewal_of_the_previous_period,
                "physical_condition": s.physical_condition,
                "check_out": check_out,
                "check_out_date": check_out_date,
                "hozor": hozor_time,
                "shoro_soreh": en.tarikhpaziresh,
                "tarikh_payan": en.tarihkepayanedore,
                "vaziat": vazit,
                "yegan_khdmati": s.unit_name,
            }
        )

        df = pd.DataFrame(list(data_list))

    # تغییر نام ستون‌ها
    df.rename(columns={
        "name": "نام",
        "family": "نام خانوادگی",
        "fathers_name": "نام پدر",
        "National_Code": "کدملی",
        "Grade": "مدرک",
        "Study_group": "رشته تحصیلی",
        "Date_of_dispatch": "تاریخ اعزام",
        "shomare_sore": "شماره دوره",
        "yegan_ezam": "یگان اعزام کننده",
        "attraction_of_the_organization": "نوع سهمیه",
        "Renewal_of_the_previous_period": "تجدید دوره",
        "physical_condition": "وضعیت جسمانی",
        "check_out": "نوع ریزش",
        "check_out_date": "تاریخ ریزش",
        "hozor": "حضور",
        "shoro_soreh": "تاریخ شروع",
        "tarikh_payan": "تاریخ پایان",
        "vaziat": "تاریخ پذیرش",
        "yegan_khdmati": "یگان خدمتی",

    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export_to_excel_list_paayne.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


def send_rank_score_page(request):
    # همه سربازان مرتب بر اساس گردان و گروهان
    in_course_soldiers = Soldier.objects.filter(
        in_coures=True, 
        willing_to_learn=True
    ).order_by(
         't_Gordan__name',
         't_battalion_group__name',
         'code_gorhan_nahai'
    )
    # تبدیل مقادیر بولین به True/False برای اطمینان
    for soldier in in_course_soldiers:
        soldier.battalion_sample = bool(soldier.battalion_sample)
        soldier.nahj_memorization = bool(soldier.nahj_memorization)
        soldier.sajjadiya_memorization = bool(soldier.sajjadiya_memorization)

    
    # صفحه‌بندی هر صفحه ۲۰ سرباز
    paginator = Paginator(in_course_soldiers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()  # 👈 خیلی مهم
    
    context = {
        'page_obj': page_obj, 
        'query_params': query_string,
    }
    
    return render(request, 'rank/send_rank_score_page.html', context)


def send_rank_score_update(request):
    input_fields_float = [
        'discipline_score',
        'basij_experience',
        'council_experience',
        'ideological_score',
        'shooting_score',
        'battalion_activity'
    ]
    input_fields_int = [
        'provincial_awards',
        'national_awards',
        'global_awards',
        'global_articles',
        'publications',
        'quran_memorization'
    ]
    checkbox_fields = [
        'battalion_sample',
        'nahj_memorization',
        'sajjadiya_memorization'
    ]

    if request.method == "POST":
        soldier_ids = {
            int(key.rsplit('_', 1)[-1])
            for key in request.POST.keys()
            if '_' in key and key.rsplit('_', 1)[-1].isdigit()
        }

        soldiers = Soldier.objects.filter(id__in=soldier_ids)

        for soldier in soldiers:
            sid = soldier.id

            # ✅ چک‌باکس‌ها
            for field in checkbox_fields:
                soldier_value = f"{field}_{sid}" in request.POST
                setattr(soldier, field, soldier_value)

            # ✅ فیلدهای عددی (اعشاری)
            for field in input_fields_float:
                key = f"{field}_{sid}"
                val = request.POST.get(key)
                setattr(soldier, field, float(val) if val not in [None, ""] else 0.0)

            # ✅ فیلدهای عددی (صحیح)
            for field in input_fields_int:
                key = f"{field}_{sid}"
                val = request.POST.get(key)
                setattr(soldier, field, int(val) if val not in [None, ""] else 0)

            soldier.basij_efficiency = request.POST.get(f"basij_efficiency_{sid}") or ''

            soldier.save()

        calculate_score_for_soldiers(soldiers)
        referer = request.META.get('HTTP_REFERER', reverse('soldiers_scores_page'))
        return redirect(referer)

    return redirect('soldiers_scores_page')


def soldiers_scores_page(request):
    user = request.user
    # 🔹 دریافت همه سربازان مجاز بر اساس دسترسی کاربر
    in_course_soldiers = get_user_soldiers(user).filter(in_coures=True,willing_to_learn=True)
    # 🔹 فیلتر گردان و گروهان از request.GET
    battalion_filter = request.GET.get('battalion_filter')
    group_filter = request.GET.get('group_filter')

    if battalion_filter:
        in_course_soldiers = in_course_soldiers.filter(t_Gordan_id=battalion_filter)
    if group_filter:
        in_course_soldiers = in_course_soldiers.filter(t_battalion_group_id=group_filter)
    # 🔹 مرتب سازی
    in_course_soldiers = in_course_soldiers.order_by(
        't_Gordan__name',
        't_battalion_group__name',
        'code_gorhan_nahai'
    )

    # 🔹 تبدیل مقادیر بولین به True/False
    for soldier in in_course_soldiers:
        soldier.battalion_sample = bool(soldier.battalion_sample)
        soldier.nahj_memorization = bool(soldier.nahj_memorization)
        soldier.sajjadiya_memorization = bool(soldier.sajjadiya_memorization)

    # 🔹 صفحه‌بندی (۱۰ سرباز در هر صفحه)
    paginator = Paginator(in_course_soldiers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 🔹 گردان‌ها و گروهان‌های مجاز برای نمایش در فیلتر
    battalions_allowed = get_user_battalions(user)
    battalion_groups_allowed = get_user_battalion_groups(user)
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()  # 👈 خیلی مهم
    
    context = {
        'page_obj': page_obj,
        'battalions': battalions_allowed,
        'groups': battalion_groups_allowed,
        'query_params':query_string
    }

    return render(request, 'courses/soldiers_scores_page.html', context)


def top_soldiers_course_page(request):
    user = request.user

    # همه سربازان مجاز برای کاربر
    soldiers = get_user_soldiers(user).filter(in_coures=True, willing_to_learn=True)

    # تعریف رتبه‌ها و آیکون‌ها
    top_ranks = [
        {'rank': '1', 'label': 'نفر اول', 'icon': 'fa-crown', 'color': '#FFD700'},
        {'rank': '2', 'label': 'نفر دوم', 'icon': 'fa-medal', 'color': '#C0C0C0'},
        {'rank': '3', 'label': 'نفر سوم', 'icon': 'fa-medal', 'color': '#CD7F32'},
    ]

    if request.method == 'POST':
        form = TopSoldiersForm(request.user, request.POST)
        if form.is_valid():
            # همه سربازانی که قبلاً top_three داشتند
            old_top_soldiers = list(Soldier.objects.filter(top_three__isnull=False))

            # پاک کردن top_three در دیتابیس
            Soldier.objects.filter(top_three__isnull=False).update(top_three=None)

            # پاک کردن top_three در حافظه برای محاسبه درست امتیاز
            for s in old_top_soldiers:
                s.top_three = None

            # محاسبه امتیاز سربازان قدیمی
            calculate_score_for_soldiers(old_top_soldiers)

            # ثبت نفرات جدید
            selected_ids = set()
            new_top_soldiers = []
            for rank in top_ranks:
                soldier_id = form.cleaned_data.get(f'soldier_{rank["rank"]}')
                if soldier_id:
                    if soldier_id in selected_ids:
                        continue  # جلوگیری از انتخاب یک نفر در چند رتبه
                    selected_ids.add(soldier_id)
                    soldier = soldiers.get(id=soldier_id)
                    soldier.top_three = rank['label']
                    soldier.save()
                    new_top_soldiers.append(soldier)

            calculate_score_for_soldiers(new_top_soldiers)

            return redirect('top_soldiers_course_page')
    else:
        form = TopSoldiersForm(request.user)

    # بارگذاری مجدد سربازان مجاز برای نمایش در قالب
    soldiers = get_user_soldiers(user).filter(in_coures=True, willing_to_learn=True)

    # نفرات فعلی برتر برای prefill select ها
    top_dict = {}
    for s in soldiers.filter(top_three__isnull=False):
        if s.top_three == 'نفر اول':
            top_dict['1'] = s.id
        elif s.top_three == 'نفر دوم':
            top_dict['2'] = s.id
        elif s.top_three == 'نفر سوم':
            top_dict['3'] = s.id

    context = {
        'soldiers': soldiers,
        'form': form,
        'top_dict': top_dict,
        'top_ranks': top_ranks,
    }

    return render(request, 'courses/top_soldiers_course_page.html', context)

def top_soldiers_gordan_page(request):
    user = request.user
    user_gordans = get_user_battalions(user)  # گردان‌های مجاز

    if request.method == 'POST':

        for gordan in user_gordans:
            soldiers = get_user_soldiers(user).filter(t_Gordan=gordan, in_coures=True, willing_to_learn=True)
            
            # سربازان قبلی نمونه گردان این گردان
            old_sample_soldiers = list(soldiers.filter(battalion_sample=True))
            for s in old_sample_soldiers:
                s.battalion_sample = False  # پاک کردن
            
            calculate_score_for_soldiers(old_sample_soldiers )
            # ثبت سه نفر انتخابی
            new_sample_soldiers = []
            for i in range(1, 4):
                soldier_id = request.POST.get(f'gordan_{gordan.id}_soldier_{i}')
                if soldier_id:
                    soldier = soldiers.get(id=soldier_id)
                    soldier.battalion_sample = True
                    soldier.save()
                    new_sample_soldiers.append(soldier)

            calculate_score_for_soldiers(new_sample_soldiers)

    gordan_tables = []
    for gordan in user_gordans:
        soldiers_qs = get_user_soldiers(user).filter(
            t_Gordan=gordan, in_coures=True, willing_to_learn=True
        )

        top_soldiers_ids = set(soldiers_qs.filter(battalion_sample=True).values_list('id', flat=True)[:3])

        soldiers = list(soldiers_qs)
        for soldier in soldiers:
            soldier.selected = soldier.id in top_soldiers_ids  
        
        top_soldiers_qs = soldiers_qs.filter(battalion_sample=True)[:3]
        top_dict = {str(idx+1): s.id for idx, s in enumerate(top_soldiers_qs)}

        gordan_tables.append({
            'gordan': {'id': gordan.id, 'name': gordan.name},
            'soldiers': soldiers,
            'top_dict':top_dict
        })


    return render(request, 'courses/top_soldiers_gordan_page.html', {'gordan_tables': gordan_tables})

def soldiers_scores_help_page(request):
    return render(request, 'courses/soldiers_scores_help.html')

from django.db.models import Max, Min,Value
def unit_problems_export_excel(request):
    soldiers = get_user_soldiers(request.user)
    soldiers = soldiers.filter(in_coures=True, willing_to_learn=True)
    soldiers = soldiers.order_by('t_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    data = []

    for s in soldiers:
        data.append({
            'National_Code':s.National_Code,
            'name':s.name,
            'family':s.family,
            'fathers_name':s.fathers_name,
            'problems_str':s.problems_str,
            'problem_unit':s.problem_unit,
            'province_name':s.province_name,
            'city_name':s.city_name,
            't_Gordan':str(s.t_Gordan),
            't_battalion_group':str(s.t_battalion_group),
            'code_gorhan_nahai':s.code_gorhan_nahai,
            'problems_str':s.problems_str,
            'problem_unit':s.problem_unit,
        })

    df = pd.DataFrame(data)
    
    df.rename(columns=
        {
            'National_Code': 'کدملی',
            'name': 'نام',
            'family': 'نام خانوادگی',
            'fathers_name': 'نام پدر',
            'problem_unit':'محل پیشنهادی',
            'problems_str':'مشکلات',
            'province_name':'استان',
            'city_name':'شهر',
            't_Gordan__name':'گردان', 
            't_battalion_group__name':'گروهان',
            'code_gorhan_nahai':'کد سازمانی',
        },
        inplace=True
    )

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=soldiers_problem_unit.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='فهرست سربازان')
        worksheet = writer.sheets['فهرست سربازان']
        worksheet.sheet_view.rightToLeft = True

    worksheet.sheet_view.rightToLeft = True

    return response

           
def soldiers_problems_page(request):
    user = request.user

    # گردان‌ها و گروهان‌ها برای فیلتر
    battalions_allowed = get_user_battalions(user)
    battalion_groups_allowed = get_user_battalion_groups(user)

    # فرم فیلتر
    filter_form = SoldierFilterForm(request.GET or None, battalions=battalions_allowed, groups=battalion_groups_allowed)

    # سربازان مجاز و در دوره جاری
    soldiers_qs = get_user_soldiers(user).filter(
        in_coures=True, 
        willing_to_learn=True
    ).order_by(
        't_Gordan__name',
        't_battalion_group__name',
        'code_gorhan_nahai'
    )   

    # اعمال فیلترها
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        battalion_filter = filter_form.cleaned_data.get('battalion_filter')
        group_filter = filter_form.cleaned_data.get('group_filter')

        if search:
            soldiers_qs = soldiers_qs.filter(
                Q(name__icontains=search) | Q(family__icontains=search) | Q(National_Code__icontains=search)
            )
        if battalion_filter:
            soldiers_qs = soldiers_qs.filter(t_Gordan_id=battalion_filter)
        if group_filter:
            soldiers_qs = soldiers_qs.filter(t_battalion_group_id=group_filter)


    # Pagination
    paginator = Paginator(soldiers_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()  # 👈 خیلی مهم
    
    # فرم مشکلات با formset
    SoldierProblemFormSet = formset_factory(SoldierProblemForm, extra=0)


    initial_data = []
    for s in page_obj:
        # مقدار اولیه از فیلد JSON problems_data
        problems_dict = s.problems_data or {}  # اگر None بود، dict خالی
        data = {
            'soldier_id': s.id,
            'description': problems_dict.get('description', '')
        }
        for field in PROBLEM_FIELDS:
            data[field] = problems_dict.get(field, False)  # مقدار هر checkbox از JSON یا False
        initial_data.append(data)

    formset = SoldierProblemFormSet(initial=initial_data)

    form_soldier_pairs = list(zip(formset.forms, page_obj))
    context = {
        'filter_form': filter_form,
        'formset': formset,
        'page_obj': page_obj,
        'form_soldier_pairs': form_soldier_pairs,  # اضافه شد
        'query_params': query_string,
        'problem_fields': [PROBLEM_LABELS[f] for f in PROBLEM_FIELDS],
        'PROBLEM_FIELDS': PROBLEM_FIELDS,
    }

    return render(request, 'courses/soldiers_problems_page.html', context)



@transaction.atomic
def soldiers_problems_update(request):
    SoldierProblemFormSet = formset_factory(SoldierProblemForm, extra=0)

    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', '/'))

    formset = SoldierProblemFormSet(request.POST)

    if not formset.is_valid():
        print(formset.errors)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # 1️⃣ جمع‌آوری IDها
    soldier_ids = [
        form.cleaned_data['soldier_id']
        for form in formset
    ]

    # 2️⃣ گرفتن سربازها با قفل ردیفی
    soldiers = (
        Soldier.objects
        .select_for_update()
        .filter(id__in=soldier_ids)
    )

    soldiers_map = {s.id: s for s in soldiers}

    updated_soldiers = []

    # 3️⃣ اعمال تغییرات در حافظه
    for form in formset:
        soldier_id = form.cleaned_data['soldier_id']
        soldier = soldiers_map.get(soldier_id)

        if not soldier:
            continue

        problems_dict = {
            field: form.cleaned_data.get(field, False)
            for field in PROBLEM_FIELDS
        }

        problems_dict['description'] = form.cleaned_data.get('description', '')

        soldier.problems_data = problems_dict
        updated_soldiers.append(soldier)

    # 4️⃣ ذخیره یک‌جا
    if updated_soldiers:
        Soldier.objects.bulk_update(
            updated_soldiers,
            ['problems_data']
        )

    return redirect(request.META.get('HTTP_REFERER', '/'))


def soldiers_problems_export_excel(request):
    user = request.user

    # ایجاد workbook و worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "مشکلات سربازان"

    # هدرها
    headers = [
        "نام و نام خانوادگی", "کد ملی", "گردان", "گروهان", "کد سازمانی"
    ]
    from .forms import PROBLEM_FIELDS, PROBLEM_LABELS
    for field in PROBLEM_FIELDS:
        headers.append(PROBLEM_LABELS.get(field, field))
    headers.append("توضیحات")

    ws.append(headers)

    # تنظیم فونت و تراز هدر
    for col_idx, col_cells in enumerate(ws.iter_cols(min_row=1, max_row=1, min_col=1, max_col=len(headers)), start=1):
        for cell in col_cells:
            cell.font = Font(bold=True, name="Vazirmatn", size=12)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
            cell.border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

    # سربازان
    soldiers = get_user_soldiers(user).filter(
        in_coures=True,
        willing_to_learn=True
    ).order_by(
        't_Gordan__name',
        't_battalion_group__name',
        'code_gorhan_nahai'
    )

    # اضافه کردن داده‌ها
    for s in soldiers:
        row = [
            f"{s.name} {s.family}",
            s.National_Code,
            s.t_Gordan.name if s.t_Gordan else '',
            s.t_battalion_group.name if s.t_battalion_group else '',
            s.code_gorhan_nahai,
        ]
        for field in PROBLEM_FIELDS:
            value = s.problems_data.get(field, False) if s.problems_data else False
            row.append("✓" if value else "")
        description = s.problems_data.get("description", "") if s.problems_data else ""
        row.append(description)
        ws.append(row)

    # استایل بدنه و راست‌چین
    for row_cells in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for cell in row_cells:
            cell.font = Font(name="Vazirmatn", size=11)
            cell.alignment = Alignment(horizontal="center", vertical="center")  # reading_order=2 -> RTL
            cell.border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

    # تنظیم خودکار عرض ستون‌ها بر اساس محتوا
    for i, column_cells in enumerate(ws.columns, start=1):
        max_length = 0
        column_letter = get_column_letter(i)
        for cell in column_cells:
            if cell.value:
                cell_length = len(str(cell.value))
                if cell_length > max_length:
                    max_length = cell_length
        ws.column_dimensions[column_letter].width = max_length + 4  # کمی فاصله اضافه برای خوانایی

    # راست‌چین کردن کل شیت
    ws.sheet_view.rightToLeft = True

    # پاسخ HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=soldiers_problems.xlsx'
    wb.save(response)
    return response

def create_full_excel(soldiers,filename='سربازان'):

    data = []
    for s in soldiers:
        data.append({
            'acceptance_code':s.acceptance_code,
            'National_Code':s.National_Code,
            'name':s.name,
            'family':s.family,
            't_Gordan__name':str(s.t_Gordan.name if s.t_Gordan else ''),
            't_battalion_group__name':str(s.t_battalion_group.name if s.t_battalion_group else ''),
            'code_gorhan_nahai':s.code_gorhan_nahai,
            'fathers_name':s.fathers_name,
            'Gordan__name':  str(s.Gordan.name if s.Gordan else ''),
            'battalion_group__name':str(s.battalion_group.name if s.battalion_group else ''),
            'code_gorhan':s.code_gorhan,
            'Amriye':s.Amriye,
            'Amriye_organization':s.Amriye_organization,
            'physical_condition':s.physical_condition,
            'Type_of_disease':s.Type_of_disease,
            'Grade':s.Grade,
            'Grade_precise':s.Grade_precise,
            'educational_level_of_the_system':s.educational_level_of_the_system,
            'Study_group':s.Study_group,
            'marital_status':s.marital_status,
            'Religion':s.Religion,
            'Date_of_birth':s.Date_of_birth,
            'place_of_birth':s.place_of_birth,
            'phone_number':s.phone_number,
            'home_phone_number':s.home_phone_number,
            'Date_of_dispatch':s.Date_of_dispatch,
            'province_name':s.province_name,
            'city_name':s.city_name,
            'Address':s.Address,
            'Place_of_Issue':s.Place_of_Issue,
            'height':s.height,
            'Weight':s.Weight,
        })
    df = pd.DataFrame(data)

    df.rename(columns={
        'National_Code': 'کدملی',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'acceptance_code': 'عدد پذیرش',
        'Gordan__name': 'نام گردان اولیه',
        'battalion_group__name': 'نام گروهان اولیه',
        'code_gorhan': 'کد سازمانی',
        't_Gordan__name': 'نام گردان',
        't_battalion_group__name': 'نام گروهان',
        'code_gorhan_nahai': 'کد سازمانی نهایی',
        'Amriye': 'امریه دار',
        'Amriye_organization': 'سازمان امریه',
        'physical_condition': 'وضعیت جسمانی',
        'Type_of_disease': 'نوع بیماری',
        'Grade': 'مقطع تحصیلی',
        'Grade_precise': 'مقطع تحصیلی دقیق',
        'educational_level_of_the_system': 'مقطع تحصیلی سامانه',
        'Study_group': 'گروه تحصیلی',
        'marital_status': 'وضعیت تاهل',
        'Religion': 'مذهب',
        'Date_of_birth': 'تاریخ تولد',
        'place_of_birth': 'محل تولد',
        'phone_number': 'شماره موبایل',
        'home_phone_number': 'شماره منزل',
        'Date_of_dispatch': 'تاریخ اعزام',
        'province_name': 'نام استان',
        'city_name': 'نام شهر',
        'Address': 'آدرس',
        'Place_of_Issue': 'محل صدور',
        'height': 'قد',
        'Weight': 'وزن',
    },inplace=True)

    # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response['Content-Disposition'] = 'attachment; filename=soldiers.xlsx'

    # with pd.ExcelWriter(response, engine='openpyxl') as writer:
    #     df.to_excel(writer, index=False, sheet_name=filename)
    #     worksheet = writer.sheets[filename]
    #     worksheet.sheet_view.rightToLeft = True

    # return response
    return get_excel_response(df, 'soldiers')




@csrf_protect
@login_required
def soldiers_tatbigh_page(request):
    # گرفتن گردان‌ها و گروهان‌هایی که کاربر اجازه مشاهده دارد
    battalions_allowed = get_user_battalions(request.user)
    groups_allowed = get_user_battalion_groups(request.user).select_related('gordan')  # select_related برای دسترسی به gordan.name


    # گرفتن گردان انتخاب شده از GET یا پیش‌فرض
    selected_battalion = request.GET.get('battalion')
    if not selected_battalion and battalions_allowed.exists():
        selected_battalion = str(battalions_allowed.first().id)

    # گرفتن گروهان انتخاب شده از GET
    selected_group = request.GET.get('group')

    if groups_allowed.exists():
        # بررسی اینکه گروهان انتخاب شده مربوط به گردان انتخاب شده هست یا نه
        valid_group = groups_allowed.filter(id=int(selected_group), gordan_id=int(selected_battalion)).first() if selected_group else None

        if valid_group:
            # اگر گروهان انتخاب شده معتبر بود، همان را نگه دار
            selected_group = str(valid_group.id)
        else:
            # اگر گروهان انتخاب شده معتبر نبود، اولین گروهان مربوط به گردان انتخابی
            first_group_in_battalion = groups_allowed.filter(gordan_id=int(selected_battalion)).first()
            if first_group_in_battalion:
                selected_group = str(first_group_in_battalion.id)
            else:
                # اگر گردان هیچ گروهان نداشت، اولین گروهان موجود در کل گروهان‌ها
                selected_group = str(groups_allowed.first().id)
    
    if selected_battalion:
        selected_battalion_obj = battalions_allowed.filter(id=selected_battalion).first()

    if selected_group:
        selected_group_obj = groups_allowed.filter(id=selected_group).first()

    # اگر درخواست POST باشد: ثبت تغییرات کد سازمانی
    if request.method == "POST":
        soldier_id = request.POST.get('soldier_id')
        new_org_code = request.POST.get('new_org_code')
        gordan_id = request.POST.get('gordan_id')
        grohan_id = request.POST.get('grohan_id')

        if soldier_id and new_org_code:
            try:
                with transaction.atomic():
                    soldier = Soldier.objects.select_for_update().get(id=soldier_id)

                    if not soldier.has_been_accepted:
                        messages.error(
                            request,
                            "سرباز پذیرش نشده! شما مجاز به جابه‌جایی سرباز نیستید"
                        )
                        return redirect(request.path + f"?battalion={selected_battalion}&group={selected_group}")

                    t_gordan = battalion.objects.get(id=gordan_id)
                    t_gorohan = battalion_group.objects.get(id=grohan_id)

                    soldier.t_Gordan = t_gordan
                    soldier.t_battalion_group = t_gorohan
                    soldier.code_gorhan_nahai = new_org_code
                    soldier.save()
                
                messages.success(request, f"تغییرات سرباز {soldier.name} با موفقیت ثبت شد.")
                return redirect(request.path + f"?battalion={selected_battalion}&group={selected_group}")
            except Soldier.DoesNotExist:
                messages.error(request, "سرباز مورد نظر یافت نشد.")
        else:
            messages.error(request, "اطلاعات ناقص است.")

    soldiers = Soldier.objects.filter()
    soldiers_in_battalion_group = (
        soldiers.annotate(
            code_gorhan_int=Cast('code_gorhan', IntegerField())
        )
        .filter(battalion_group=selected_group)
        .order_by('code_gorhan_int')
    )

    soldiers_in_t_battalion_group = (
        soldiers.annotate(
            code_gorhan_nahai_int=Cast('code_gorhan_nahai', IntegerField()),
            code_gorhan_int=Cast('code_gorhan', IntegerField()),
        )
        .filter(t_battalion_group=selected_group)
        .order_by('code_gorhan_nahai_int', 'code_gorhan_int')
    )
    
    soldiers_no_t_battalion_group = (
        soldiers_in_battalion_group.annotate(
            code_gorhan_nahai_int=Cast('code_gorhan_nahai', IntegerField()),
            code_gorhan_int=Cast('code_gorhan', IntegerField()),
        )
        .filter(t_battalion_group=None)
        .order_by('code_gorhan_nahai_int', 'code_gorhan_int')
    )
    soldiers_pre_t = soldiers.filter(has_been_accepted=True,in_coures=True) 
    ctx = user_access_context(request)
    perms = ctx['permissions']
    en = ctx['en']
    # یا مستقیماً از context template استفاده کنید
    access_edit = perms['dep'].get('niru_ensani', False)
    if not access_edit:
        access_edit = perms['dep'].get('gordan', False)
        if en.tatbigh:
            access_edit = False   
    
    context = {
        'soldiers_in_battalion_group':soldiers_in_battalion_group,
        'soldiers_in_t_battalion_group':soldiers_in_t_battalion_group,
        'soldiers_no_t_battalion_group':soldiers_no_t_battalion_group,
        'battalions': battalions_allowed,
        'groups': groups_allowed,
        'selected_battalion': str(selected_battalion),
        'selected_group': str(selected_group),
        'selected_group_name': str(selected_group),
        'selected_battalion_name': selected_battalion_obj.name if selected_battalion_obj else None,
        'selected_group_name': selected_group_obj.name if selected_group_obj else None,
        'soldiers': soldiers,
        'soldiers_pre_t':soldiers_pre_t,
        'access_edit':access_edit
    }
    
    if request.method == "GET":
        tab    = request.GET.get('tab')
        action = request.GET.get('action')
        s = []
        if tab =='before-tab':
            s = soldiers_in_battalion_group
        if tab == 'after-tab':
            s = soldiers_in_t_battalion_group
        if tab == 'notatbigh-tab':
            s = soldiers_no_t_battalion_group


        if action == 'exportPrint':
            context = {'soldiers':s,'action':action,'tab':tab}
            return render(request, 'courses/soldiers_tatbigh_print.html', context)
        if action == 'exportExcel':
            return create_full_excel(soldiers=s)
    
    return render(request, 'courses/soldiers_tatbigh_page.html', context)



def remove_soldier_from_tatbigh(request, pk):
    if request.method == "POST":
        try:
            soldier = Soldier.objects.get(id=pk)
            soldier.t_Gordan = None
            soldier.t_battalion_group = None
            soldier.code_gorhan_nahai = None
            soldier.save()

            messages.success(request, "سرباز با موفقیت از تطبیق حذف شد.")
        except Soldier.DoesNotExist:
            messages.error(request, "سرباز مورد نظر پیدا نشد.")
        except Exception:
            messages.error(request, "خطایی در حذف تطبیق سرباز رخ داد.")

    # بازگشت دقیقاً به همان URL قبلی
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def test_salamat_rawan(request):
    soldiers = Soldier.objects.filter( physical_condition_date_created__isnull=False).order_by('-physical_condition_date_created')
  # تعداد هر وضعیت بررسی
    inspection_filters = [
        {'key': 'all', 'label': 'همه', 'count': soldiers.count()},
        {'key': 'confirmed', 'label': 'تایید شده', 'count': soldiers.filter(physical_condition_Inspection_test=True).count()},
        {'key': 'unconfirmed', 'label': 'تایید نشده', 'count': soldiers.filter(physical_condition_Inspection_test=False).count()},
        {'key': 'proccess', 'label': 'در حال بررسی', 'count': soldiers.filter(physical_condition_Inspection_test__isnull=True).count()},
    ]
    
    inspection_filter = request.GET.get('inspection_filter', 'all')
    if inspection_filter == 'unconfirmed':
        soldiers = soldiers.filter(physical_condition_Inspection_test=False)
    elif inspection_filter == 'confirmed':
        soldiers = soldiers.filter(physical_condition_Inspection_test=True)
    elif inspection_filter == 'proccess':
        soldiers = soldiers.filter(physical_condition_Inspection_test__isnull=True)
    # جستجو
    query = request.GET.get('q', '')
    if query:
        soldiers = soldiers.filter(name__icontains=query) | soldiers.filter(family__icontains=query) | soldiers.filter(National_Code__icontains=query)

    # Pagination
    paginator = Paginator(soldiers, 10)  # هر صفحه 10 سرباز
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = TestSalamatRavanForm(request.POST)
        if form.is_valid():
            soldier = form.cleaned_data['soldier']

            # مقدار قبلی وضعیت جسمانی
            soldier.physical_condition_prev_test = soldier.physical_condition
            # وضعیت سلامت روان
            pct_value = form.cleaned_data['physical_condition_test']
            pct_label = dict(physical_condition_list).get(int(pct_value), 'نامشخص')
            soldier.physical_condition_test = pct_label

            # توضیحات
            soldier.physical_condition_description_test = form.cleaned_data['physical_condition_description_test']

            # نوع بیماری
            todt_value = form.cleaned_data['Type_of_disease_test']
            try:
                todt_int = int(todt_value)
                todt_label = dict(Type_of_disease_list).get(todt_int)
                soldier.Type_of_disease_test = todt_label or todt_value
            except ValueError:
                soldier.Type_of_disease_test = todt_value

            # تاریخ‌ها
            soldier.physical_condition_date_test = form.cleaned_data['physical_condition_date_test'] or timezone.now().date()
            soldier.physical_condition_date_created = timezone.now()

            soldier.save()
            messages.success(request, "✅ اطلاعات تست سلامت روان با موفقیت ثبت شد.")
            return redirect('test_salamat_rawan')
        else:
            messages.error(request, "⚠️ فرم معتبر نیست، لطفاً دوباره بررسی کنید.")
    else:
        form = TestSalamatRavanForm()

    
    return render(request, 'courses/test_salamat_rawan.html', {
        'form': form,
        'soldiers': page_obj,
        'page_obj':page_obj,
        'inspection_filter': inspection_filter,
        'query': query,
        'inspection_filters': inspection_filters,  # <-- ارسال تعدادها

    })




@login_required
def test_salamat_ravan_actions(request, soldier_id=None, action=None):
    """
    مدیریت عملیات تست سلامت روان:
    - عملیات تکی: delete, confirm, unconfirm
    - عملیات دسته‌ای (صفحه یا همه): confirmall, unconfirmall, confirmall_in_page, unconfirmall_in_page
    """
    # --- عملیات دسته‌ای از طریق POST ---
    if request.method == "POST" and 'soldier_ids' in request.POST:
        action = request.POST.get('action')
        if action not in ['confirmall', 'unconfirmall', 'confirmall_in_page', 'unconfirmall_in_page','processing_page','processing_all']:
            messages.error(request, "عملیات دسته‌ای نامعتبر است.")
            return redirect('test_salamat_rawan')
        soldiers = Soldier.objects.filter(physical_condition_date_created__isnull=False)
        print(action)
        if  action in ["unconfirmall_in_page", "confirmall_in_page",'processing_page']:
            soldier_ids = request.POST.getlist('soldier_ids')
            soldiers = Soldier.objects.filter(id__in=soldier_ids)
        for soldier in soldiers:
            if action in ["processing_all", "processing_page",'']:
                soldier.in_proccess_test_salamat_ravan()
            if action in ["confirmall", "confirmall_in_page",'']:
                soldier.confirm_test_salamat_ravan()
            elif action in ["unconfirmall", "unconfirmall_in_page",'']:
                soldier.unconfirm_test_salamat_ravan()

        messages.success(request, f"عملیات {action} با موفقیت روی {len(soldiers)} سرباز انجام شد.")
        return redirect('test_salamat_rawan')

    # --- عملیات تکی ---
    if soldier_id is None or action is None:
        messages.error(request, "پارامترهای لازم ارسال نشده‌اند.")
        return redirect('test_salamat_rawan')

    soldier = get_object_or_404(Soldier, id=soldier_id)

    if action == "delete":
        soldier.delete_test_salamat_ravan()
        messages.success(request, f"تست سلامت روان سرباز {soldier.name} {soldier.family} حذف شد.")

    elif action == "confirm":
        soldier.confirm_test_salamat_ravan()
        messages.success(request, f"تست سلامت روان سرباز {soldier.name} {soldier.family} تایید شد.")

    elif action == "unconfirm":
        soldier.unconfirm_test_salamat_ravan()
        messages.success(request, f"تست سلامت روان سرباز {soldier.name} {soldier.family} عدم تایید شد.")
    elif action == "processing":
        soldier.in_proccess_test_salamat_ravan()
        messages.success(request, f"تست سلامت روان سرباز {soldier.name} {soldier.family} عدم تایید شد.")
 
    else:
        messages.error(request, "عملیات نامعتبر است.")

    return redirect('test_salamat_rawan')


@login_required
@require_GET
def get_soldier_by_national_code(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({"error": "کد ملی ارسال نشده است."}, status=400)

    try:
        soldier = Soldier.objects.get(National_Code=code)

        data = {
            "id": soldier.id,
            "National_Code": soldier.National_Code,
            "name": soldier.name or "—",
            "family": soldier.family or "—",
            "Gordan": soldier.Gordan.name if soldier.Gordan else "—",
            "t_Gordan": soldier.t_Gordan.name if soldier.t_Gordan else "—",
            "battalion_group": soldier.battalion_group.name if soldier.battalion_group else "—",
            "t_battalion_group": soldier.t_battalion_group.name if soldier.t_battalion_group else "—",
            "code_paziresh": soldier.code_paziresh or "—",
            "code_gorhan": soldier.code_gorhan or "—",
            "code_gorhan_nahai": soldier.code_gorhan_nahai or "—",
            "fathers_name": soldier.fathers_name or "—",
            "Grade": soldier.Grade or "—",
        }
        return JsonResponse(data)
    except Soldier.DoesNotExist:
        return JsonResponse({"error": "سربازی با این کد ملی یافت نشد."}, status=404)

import re
@login_required
def soldiers_avatar_page(request):
    # 🟦 دریافت گردان و گروهان‌های مجاز
    battalions_allowed = get_user_battalions(request.user)
    groups_allowed = get_user_battalion_groups(request.user).select_related('gordan')
    en = EnsaniSettings.objects.first()

    selected_battalion = request.GET.get('battalion')
    if not selected_battalion and battalions_allowed.exists():
        selected_battalion = str(battalions_allowed.first().id)

    selected_group = request.GET.get('group')

    if groups_allowed.exists():
        valid_group = (
            groups_allowed.filter(id=int(selected_group), gordan_id=int(selected_battalion)).first()
            if selected_group else None
        )
        if valid_group:
            selected_group = str(valid_group.id)
        else:
            first_group = groups_allowed.filter(gordan_id=int(selected_battalion)).first()
            if first_group:
                selected_group = str(first_group.id)
            else:
                selected_group = str(groups_allowed.first().id)

    selected_battalion_obj = battalions_allowed.filter(id=selected_battalion).first() if selected_battalion else None
    selected_group_obj = groups_allowed.filter(id=selected_group).first() if selected_group else None

    soldiers = get_user_soldiers(request.user).annotate(
        code_gorhan_nahai_int=Cast('code_gorhan_nahai', IntegerField()),
        code_gorhan_int=Cast('code_gorhan', IntegerField()),
    )
    
    # وقتی کاربر فایل ZIP آپلود می‌کند
    if request.method == "POST" and request.FILES.get("zip_file"):
        uploaded_zip = request.FILES["zip_file"]
        results = []  # برای گزارش اکسل
        action = request.POST.get('formats','')
        
        def organization_code_soldier(query_name=''):
            query_name = query_name.strip()
            query_name = query_name.replace('.', ' ')
            query_name = query_name.replace('-', ' ')
            query_name = query_name.replace('_', ' ')
            group_code,code_gorhan = query_name.split(' ')
            gordan  = group_code[0].strip()
            gorohan = group_code[1].strip()
            code_gorhan = code_gorhan.strip()
            if en.tatbigh:
                soldier =  Soldier.objects.filter(
                    t_Gordan__gcode=gordan,
                    t_battalion_group__name=gorohan,
                    code_gorhan_nahai=code_gorhan
                )
            else:
                soldier = Soldier.objects.filter(
                    Gordan__gcode=gordan,
                    battalion_group__name=gorohan,
                    code_gorhan=code_gorhan
                )

            s = soldier.first()
            print(s)
            return s
        # باز کردن فایل ZIP
        with zipfile.ZipFile(uploaded_zip, "r") as z:
            for filename in z.namelist():
                if filename.endswith(("/", "\\")):  # رد کردن پوشه‌ها
                    continue
                
                # استخراج نام فایل بدون پسوند (کد ملی)
                query_name = os.path.splitext(os.path.basename(filename))[0]
                file_data = z.read(filename)
                file_obj = io.BytesIO(file_data)
                file_obj.name = os.path.basename(filename)
                try:
                    if action == 'organization_code':
                        soldier = organization_code_soldier(query_name)
                    elif action == 'paziresh_code':
                        soldier = Soldier.objects.get(code_paziresh=query_name)
                    else:
                        soldier = Soldier.objects.get(National_Code=query_name)
                    
                    try:
                        print(soldier)
                        if not soldier:
                            results.append({ "نام فایل": query_name, "وضعیت": "سرباز یافت نشد" })
                        elif not soldier in soldiers:
                            results.append({ "نام فایل": query_name, "وضعیت": "دسترسی غیر مجاز" })
                        else:
                            soldier.save_avatar(file_obj)
                            results.append({ "نام فایل": query_name, "وضعیت": "ذخیره شد" })
                    except Exception as e:
                        
                        results.append({ "نام فایل": query_name, "وضعیت": f"خطا در ذخیره‌سازی: {str(e)}" })
                except Soldier.DoesNotExist as e:
                    print(e)
                    results.append({ "نام فایل": query_name, "وضعیت": "کد ملی یافت نشد" })

        # ساخت DataFrame از نتایج
        df = pd.DataFrame(results)

        # تولید اکسل در حافظه
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="گزارش")

        excel_buffer.seek(0)

        # ساخت پاسخ برای دانلود اکسل
        response = HttpResponse(
            excel_buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="soldiers_report.xlsx"'
        return response
    

    if en.tatbigh:
        soldiers = soldiers.filter(t_battalion_group=selected_group).order_by('code_gorhan_nahai_int', 'code_gorhan_int')
    else:
        soldiers = soldiers.filter(battalion_group=selected_group).order_by('code_gorhan_int')

    context = {
        'soldiers': soldiers,
        'battalions': battalions_allowed,
        'groups': groups_allowed,
        'selected_battalion': str(selected_battalion),
        'selected_group': str(selected_group),
        'selected_battalion_name': selected_battalion_obj.name if selected_battalion_obj else None,
        'selected_group_name': selected_group_obj.name if selected_group_obj else None,
    }
    return render(request, 'courses/soldiers_avatar_page.html', context)



ideological_fields = [
    {
        "score": "ideological_score_start",
        "assessment": "ideological_score_start_assessment",
        "label": "شروع دوره"
    },
    {
        "score": "ideological_score",
        "assessment": "ideological_score_assessment",
        "label": "میان دوره"
    },
    {
        "score": "ideological_score_end",
        "assessment": "ideological_score_end_assessment",
        "label": "پایان دوره"
    }
]

from .utils import get_battalion_group_context

def soldiers_ideological_assessment_page(request):
    base_soldiers = Soldier.objects.filter(has_been_accepted=True)

    context = get_battalion_group_context(request, base_soldiers)

    page_context ={
        'assessments': IdeologicalAssessment.objects.all(),
        'ideological_fields': ideological_fields,
    }
    context.update(page_context)
    template_name = 'courses/soldiers_ideological_assessment_page.html'
    return render(request,template_name,context)

    
def soldiers_ideological_assessment_delete(request):
    pass


def assessment_add(request):
    if request.method == 'POST':
        form = IdeologicalAssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ارزیاب با موفقیت ثبت شد.')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نیست.')

    return redirect('soldiers_ideological_assessment_page')

def assessment_edit(request, pk):
    assessment = get_object_or_404(IdeologicalAssessment, pk=pk)

    if request.method == 'POST':
        form = IdeologicalAssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات ارزیاب با موفقیت ویرایش شد.')
        else:
            messages.error(request, 'ویرایش انجام نشد. داده‌ها را بررسی کنید.')

    return redirect('soldiers_ideological_assessment_page')

def assessment_delete(request):
    if request.method == 'POST':
        assessment_id = request.POST.get('id')
        assessment = get_object_or_404(IdeologicalAssessment, pk=assessment_id)
        assessment.delete()
        messages.warning(request, 'ارزیاب حذف شد.')

    return redirect('soldiers_ideological_assessment_page')


def soldiers_ideological_assessment_save(request):
    if request.method != "POST":
        return redirect('soldiers_ideological_assessment_page')

    form = IdeologicalAssessmentBulkForm(request.POST)

    if not form.is_valid():
        print(form.errors)  # برای دیباگ
        messages.error(request, "مقادیر ارزیابی نامعتبر هستند")
        return redirect('soldiers_ideological_assessment_page')

    with transaction.atomic():
        soldiers = Soldier.objects.select_for_update().filter(id__in=form.cleaned_bulk_data.keys())
        soldier_map = {s.id: s for s in soldiers}

        for sid, data in form.cleaned_bulk_data.items():
            soldier = soldier_map.get(sid)
            if not soldier:
                continue

            for field, value in data.items():
                # تبدیل مناسب انواع
                if field in form.CHECKBOX_FIELDS:
                    value = bool(value)
                elif field in form.SCORE_FIELDS:
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        value = 0.0
                elif field in form.ASSESSMENT_FIELDS:
                    value = value.strip() if value else None

                setattr(soldier, field, value)

        update_fields = list(form.SCORE_FIELDS | form.ASSESSMENT_FIELDS | form.CHECKBOX_FIELDS)
        Soldier.objects.bulk_update(soldiers, update_fields)

    messages.success(request, "ارزیابی‌ها با موفقیت ذخیره شد")
    return redirect('soldiers_ideological_assessment_page')

def weapon_score_page(request):
    base_soldiers = Soldier.objects.filter(has_been_accepted=True)
    context = get_battalion_group_context(request, base_soldiers)
    template_name = 'courses/weapon_score_page.html'
    return render(request,template_name,context)

def soldiers_training_transcript_page(request):
    base_soldiers = Soldier.objects.filter(has_been_accepted=True)

    context = get_battalion_group_context(request, base_soldiers)

    items = [
        {
            "title": "خروجی اکسل",
            'base_url':'soldiers_training_transcript_export_excel',
            "children": context['nodes'],
        },
        {
            "title": "چاپ کارنامه",
            'base_url':'soldiers_training_transcript_print',
            "children": context['nodes'],
        },
        # {
        #     "title": "چاپ فهرست",
        #     'base_url':'',
        #     'q':'#',
        #     "children": context['nodes'],
        # },
    ]
    # context.soldiers
    page_context = {
        'training_fields':SoldierTrainingRecord.training_fields(),
        'items':items,
        'parent_base_url': '',
    }
    context.update(page_context)
    template_name = 'courses/soldiers_training_transcript_page.html'
    return render(request,template_name,context)


def quick_excel_soldiers(soldiers):
    headers = [
        'وضعیت سرباز',
        'تسویه حساب',
        "کد ملی",
        "نام",
        "نام خانوادگی",
        "نام پدر",
        'محل صدور',
        'تاریخ تولد',
        'محل تولد',
        "وضعیت سلامت",
        'کمیسیون پزشکی',
        'امریه',
        'سازمان امریه',
        "گردان نهای",
        "گروهان نهای",
        "کد سازمانی نهای",
        "گردان اولیه ",
        "گروهان اولیه",
        "کد سازمانی اولیه",
        'مقطع تحصیلی',
        'مقطع تحصیلی دقیق',
        'مقطع تحصیلی سامانه',
        'رشته تحصیلی',
        'متاهل',
        'مذهب',
        'شماره تماس',
        'شماره منزل',
        'استان',
        'شهر',
        'آدرس'
    ]

    # آماده‌سازی داده‌ها
    data = []
    for s in soldiers:
        # tatbigh no
        g_name = s.Gordan.name if s.Gordan else ''
        b_name = s.battalion_group.name if s.battalion_group else ''
        # tatbigh
        tg_name = s.t_Gordan.name if s.t_Gordan else ''
        tb_name = s.t_battalion_group.name if s.t_battalion_group else ''
        kf= "درحال اموزش"
        if s.Sufficiency_of_mobilization: 
            kf= "کفایت از بسیج"
        if s.Previous_service_record:
            kf= "خدمت دار قبلی"
            
        row = [
            kf,
            'بله' if s.IsCheckout else 'خیر',
            s.National_Code,
            s.name,
            s.family,
            s.fathers_name,
            s.Place_of_Issue,
            s.Date_of_birth,
            s.physical_condition,
            s.place_of_birth,
            '*' if s.Amriye else '',
            s.Amriye_organization,
            s.the_medical_commission,
            tg_name,
            tb_name,
            s.code_gorhan_nahai,
            g_name,
            b_name,
            s.code_gorhan,
            s.Grade,
            s.Grade_precise,
            s.educational_level_of_the_system,
            s.Study_group,
            s.marital_status,
            s.Religion,
            s.phone_number,
            s.home_phone_number,
            s.city_name,
            s.province_name,
            s.Address
        ]
        data.append(row)
    # استفاده از تابع generate_excel
    return generate_excel(headers, data, filename="Soldiers_Quick_Export")


def soldiers_kefayat_quick_export_excel(request):
    _type = request.GET.get('type')
    
    if  _type == "basij":    
        soldiers = Soldier.objects.filter(Q(Sufficiency_of_mobilization=True))
    elif _type == "khedmat_ghabli":
        soldiers = Soldier.objects.filter(Q(Previous_service_record=True))
    else  :
        soldiers = Soldier.objects.filter(Q(Sufficiency_of_mobilization=True)|Q(Previous_service_record=True))

    return quick_excel_soldiers(soldiers)



def soldiers_quick_export_excel(request):
    b = request.GET.get('b')
    g = request.GET.get('g')
    # گرفتن سربازان با رکورد آموزشی
    soldiers_qs = Soldier.objects.all()
    soldiers = get_filtered_soldiers(soldiers_qs, battalion=b, group=g)

    return quick_excel_soldiers(soldiers)

def soldiers_healthy_quick_export_excel(request):
    b = request.GET.get('b')
    g = request.GET.get('g')
    physical_condition = request.GET.get('physical_condition','')
    # گرفتن سربازان با رکورد آموزشی
    soldiers_qs = Soldier.objects.all()
    
    if physical_condition == "healthy":
        soldiers_qs = soldiers_qs.filter(physical_condition='سالم')
    elif physical_condition == "moaf":
        soldiers_qs = soldiers_qs.filter(physical_condition='معاف از رزم')
    elif physical_condition == "grobe":
        soldiers_qs = soldiers_qs.filter(Q(physical_condition='گروه ب')|Q(physical_condition='معاف+گروه ب'))
    else:
        soldiers_qs.filter(physical_condition='نامشخص')
    
    
    soldiers = get_filtered_soldiers(soldiers_qs, battalion=b, group=g)
    
    return quick_excel_soldiers(soldiers)



def soldiers_training_transcript_export_excel(request):
    b = request.GET.get('b')
    g = request.GET.get('g')

    # گرفتن سربازان با رکورد آموزشی
    soldiers_qs = Soldier.objects.filter(training_record__isnull=False).select_related('training_record')
    soldiers = get_filtered_soldiers(soldiers_qs, battalion=b, group=g)

    en = EnsaniSettings.objects.first()

    # آماده‌سازی هدرها
    headers = [
        "نام",
        "نام خانوادگی",
        "نام پدر",
        "کد ملی",
        "گردان",
        "گروهان",
        "کد سازمانی",
        "مرحله ۱ تیراندازی",
        "مرحله ۲ تیراندازی",
        "مرحله ۳ تیراندازی",
        "مرحله ۴ تیراندازی",
        "میانگین تیراندازی",
        "نمره تاکتیک",
        "آمادگی جسمانی",
        "انضباط",
        "میانگین نهایی",
    ]

    # آماده‌سازی داده‌ها
    data = []
    for s in soldiers:
        if en.tatbigh:
            g_name = s.t_Gordan.name if s.t_Gordan else ''
            b_name = s.t_battalion_group.name if s.t_battalion_group else ''
        else:
            g_name = s.Gordan.name if s.Gordan else ''
            b_name = s.battalion_group.name if s.battalion_group else ''

        row = [
            s.name,
            s.family,
            s.fathers_name,
            s.National_Code,
            g_name,
            b_name,
            s.current_code,
            getattr(s.training_record, 'shooting_stage_1', ''),
            getattr(s.training_record, 'shooting_stage_2', ''),
            getattr(s.training_record, 'shooting_stage_3', ''),
            getattr(s.training_record, 'shooting_stage_4', ''),
            getattr(s.training_record, 'shooting_avg', ''),
            getattr(s.training_record, 'tactic_score', ''),
            getattr(s.training_record, 'physical_fitness_score', ''),
            getattr(s.training_record, 'military_discipline_score', ''),
            getattr(s.training_record, 'final_average', ''),
        ]
        data.append(row)

    # استفاده از تابع generate_excel
    return generate_excel(headers, data, filename="Soldiers_Training_Transcript")


def soldiers_training_transcript_export_print(request):
    pass

def soldiers_training_transcript_print(request):
    b = request.GET.get('b')
    g = request.GET.get('g')
    soldiers_qs = Soldier.objects.all()
    soldiers = get_filtered_soldiers(soldiers_qs, battalion=b, group=g)
    context = { 
        "soldiers": soldiers, 
        "b": b,  
        "g": g,
    }
    return render(request, "courses/soldiers_training_transcript_print.html", context)


def soldiers_training_transcript_save(request):
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', 'soldiers_training_transcript_page'))

    form = BulkDynamicForm(data=request.POST)
    form.INT_FIELDS = SoldierTrainingRecord.EDITABLE_FIELDS

    if not form.is_valid():
        return redirect('soldiers_training_transcript_page')

    cleaned_data = form.cleaned_bulk_data
    if not cleaned_data:
        return redirect('soldiers_training_transcript_page')

    soldier_ids = list(cleaned_data.keys())

    # fetch کلی رکوردهای موجود
    existing_records = SoldierTrainingRecord.objects.filter(
        soldier_id__in=soldier_ids
    ).select_related('soldier')

    existing_map = {r.soldier_id: r for r in existing_records}

    to_create = []
    to_update = []
    print(to_create,to_update)

    with transaction.atomic():
        for sid, fields in cleaned_data.items():
            # فقط فیلدهای editable
            update_data = {f: v for f, v in fields.items() if f in SoldierTrainingRecord.EDITABLE_FIELDS}
            if not update_data:
                continue  # رکورد خالی → skip

            record = existing_map.get(sid)
            if record:
                # رکورد موجود → setattr
                for f, v in update_data.items():
                    setattr(record, f, v)
                # محاسبه readonly ها
                record.shooting_avg = record.calculate_shooting_avg()
                record.final_average = record.calculate_final_average()
                # اضافه کردن به لیست update
                to_update.append(record)
            else:
                # رکورد جدید
                temp = SoldierTrainingRecord(
                    soldier_id=sid,
                    **update_data
                )
                temp.shooting_avg = temp.calculate_shooting_avg()
                temp.final_average = temp.calculate_final_average()
                to_create.append(temp)

        # bulk create برای رکوردهای جدید
        if to_create:
            SoldierTrainingRecord.objects.bulk_create(to_create)

        # bulk update برای رکوردهای موجود
        if to_update:
            update_fields = SoldierTrainingRecord.EDITABLE_FIELDS + SoldierTrainingRecord.READONLY_FIELDS
            SoldierTrainingRecord.objects.bulk_update(to_update, update_fields)

    return redirect(request.META.get('HTTP_REFERER', 'soldiers_training_transcript_page'))
