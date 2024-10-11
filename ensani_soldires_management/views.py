from django.shortcuts import render
from django.views import View

from ensani_soldires_management.forms import FormUpdateGordan, Formjazbi
from soldiers.models import Soldier
from ensani_letter.models import NormalLetterModels
import pandas as pd
from django.http import HttpResponse
import openpyxl
from battalions.models import battalion, battalion_group


# Create your views here.


def soldier_search(request):
    query = request.GET.get('name')
    family = request.GET.get('family')
    national_code = request.GET.get('national_code')
    physical_condition = request.GET.get('physical_condition')
    marital_status = request.GET.get('marital_status')
    religion = request.GET.get('religion')
    acceptance_code = request.GET.get('acceptance_code')

    soldiers = Soldier.objects.all()

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

    context = {
        'results': soldiers
    }

    return render(request, 'ensani_soldires_management/soldier_search.html', context)


def soldire_details(request, code):
    if request.method == "GET":
        soldire = Soldier.objects.filter(National_Code=code).first()
        normalLetter = NormalLetterModels.objects.filter(soldire=soldire).all()
        context = {'soldier': soldire, 'normalLetter': normalLetter}
        return render(request, 'ensani_soldires_management/soldire_details.html', context)


def export_to_excel_list_hazer_be_khdmat(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'acceptance_code', 'name', 'family',
        'National_Code', 't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai').order_by(
        'acceptance_code')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'acceptance_code': 'کد پذیرش',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'National_Code': 'کدملی',
        't_Gordan__name': 'نام گردان',
        't_battalion_group__name': 'نام گروهان',
        'code_gorhan_nahai': 'کد گروهان'
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_hazer_be_khdmat.xlsx'

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


class exel_update_gordan(View):
    def get(self, request):
        form = FormUpdateGordan()
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_gordan.html', cx)

    def post(self, request):
        form = FormUpdateGordan(request.POST, request.FILES or None)
        cx = {'form': form}

        if form.is_valid():
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
                        t_gordan = battalion.objects.filter(name__icontains=one_soldire_list[7]).first()
                        t_gorohan = battalion_group.objects.filter(gordan=t_gordan,
                                                                   name__icontains=one_soldire_list[8]).first()
                        find_soldire.t_Gordan = t_gordan
                        find_soldire.t_battalion_group = t_gorohan
                        code_nahai_gorohan = one_soldire_list[9]
                        find_soldire.code_gorhan_nahai = int(code_nahai_gorohan)
                        find_soldire.tatbigh = True
                        find_soldire.save()

        return render(request, 'ensani_soldires_management/update_gordan.html', cx)


class exel_jazbi(View):
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


def export_to_excel_list_sarbvaz_test_salamat_ravan(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                      physical_condition="سالم", attraction_of_the_organization='هیچکدام').values(
        'acceptance_code', 'name', 'family',
        'National_Code', 't_Gordan__name', 't_battalion_group__name',
        'code_gorhan_nahai').order_by(
        'acceptance_code')

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


def PrintPosheNokhodi(request):
    in_course_soldire = Soldier.objects.filter(in_coures=True, willing_to_learn=True).order_by('t_Gordan__name',
                                                                                               't_battalion_group__name',

                                                                                               'code_gorhan_nahai')
    cx = {'soldires': in_course_soldire}
    return render(request, 'ensani_soldires_management/print_poshe_nokhodi.html', cx)
