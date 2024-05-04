from datetime import datetime

import jdatetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from battalions.models import battalion, battalion_group
from soldiers.models import Soldier as sarbaz
from .forms import SarbazCodeMeli, FormSoldiers, FormSoldiersCreate


def paziresh_code_meli(request, *args, **kwargs):
    sarbaz_code_meli = SarbazCodeMeli(request.POST or None)
    if sarbaz_code_meli.is_valid():
        code_meli = sarbaz_code_meli.cleaned_data.get('code_meli')
        return HttpResponseRedirect(reverse("get_sarbaz", args=[code_meli]))

    return render(request, 'soldiers/paziresh_idcode_view.html', context={'SarbazCodeMeli': sarbaz_code_meli})


class sabte_paziresh(LoginRequiredMixin, View):
    template = 'soldiers/sabte_paziresh_view.html'

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(National_Code=pk).first()
        return render(request, self.template, cx)

    def post(self, request):
        cx = {}
        return render(request, self.template, cx)


class moarefi_be_gordan_va_sater(LoginRequiredMixin, View):
    template = 'soldiers/moarefi_be_gordan_va_sater.html'

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(pk=pk).first()
        time = my_sarbaz.tarikh_paziresh.time()
        date = my_sarbaz.tarikh_paziresh.date()
        cx = {'sarbaz': my_sarbaz, 'time': time, 'date': date}
        return render(request, self.template, cx)

    def post(self, request, pk):
        cx = {}
        return render(request, self.template, cx)


class sater(LoginRequiredMixin, View):

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(National_Code=pk).first()
        cx = {'sarbaz': my_sarbaz}
        return render(request, 'soldiers/sater_adi_page.html', cx)


province_name_list = [
    (1, 'مازندران'),
    (3, 'خراسان رضوی'),
    (4, 'خراسان جنوبی'),
    (5, 'گلستان'),
    (6, 'گیلان'),
    (7, 'تهران'),
    (8, 'سمنان'),
    (9, 'البرز'),
    (10, 'یزد'),
    (11, 'هرمزگان'),
    (12, 'کردستان'),
    (13, 'ایلام'),
    (14, 'همدان'),
    (15, 'زنجان'),
    (16, 'کردستان'),
    (17, 'کرمان'),
    (18, 'لرستان'),
    (19, 'اردبیل'),
    (20, 'مرکزی'),
    (21, 'سیستان و بلوچستان'),
    (22, 'آذربایجان غربی'),
    (23, 'قزوین'),
    (24, 'اصفهان'),
    (25, 'آذربایجان شرقی'),
    (26, 'قم'),
    (27, 'کهگیلویه و بویر احمد'),
    (28, 'فارس'),
    (29, 'چهارمحال و بختیاری'),
    (30, 'کرمانشاه'),
    (31, 'خوزستان'),
    (32, 'نامشخص'),
]
educational_level_of_the_system_list = [
    (1, "حوزوی سطح ىو اهل سنت"),
    (2, "دکتری پزشکی پیوسته(دیپلم به دکتری)"),
    (3, "دکتری تخصصی پزشکی ناپیوسته"),
    (4, "فوق دیپلم پزشکی"),
    (5, "فوق دیپلم غیر پزشکی"),
    (6, "فوق دیپلم فنی و حرفه ای"),
    (7, "فوق لیسانس پزشکی ناپیوسته"),
    (8, "فوق لیسانس غیرپزشکی ناپیوسته"),
    (9, "لیسانس"),
    (10, "لیسانس پزشکی پیوسته"),
    (11, "لیسانس غیر پزشکی پیوسته"),
    (12, "لیسانس غیرپزشکی ناپیوسته"),
    (13, "دیپلم"),
    (14, 'پایه یکم'),
    (15, 'پایه دوم'),
    (16, 'پایه سوم'),
    (17, 'پایه چهارم'),
    (18, 'پایه پنج'),
    (19, 'پایه ششم'),
    (20, 'پایه هفت'),
    (21, 'پایه هشتم'),
    (22, 'پایه نهم'),
    (23, 'پایه دهم'),
    (24, 'پایه یازدهم'),
    (25, 'پایه دوازدهم'),
]
Renewal_of_the_previous_period_list = [(1, 'المهدی'), (2, 'شیراز')]
Reason_for_renewing_the_course_list = [(1, 'کمیسیون پزشکی'), (2, 'فرار'), (3, 'تجدید دوره'), (4, 'انضباطی'),
                                       (5, 'نامشخص')]
attraction_of_the_organization_list = [(1, 'هیچکدام'), (2, 'جذبی سپاه و مامور'), (3, 'جذبی نیروی زمینی'), ]
Sutter_list = [(1, 'مجوز دارد'), (2, 'نیاز به بررسی'), (3, 'مجوز ندارد')]
Sufficiency_of_mobilization_list = [(1, 'خیر'), (2, 'بله')]
marital_status_list = [(1, 'مجرد'), (2, 'متاهل'), (3, 'نامشخص')]
Religion_list = [(1, 'شیعه'), (2, 'اهل تسنن'), (3, 'نامشخص')]
physical_condition_list = [(1, 'سالم'), (2, 'معاف از رزم'), (3, 'گروه ب'), (4, 'معاف+گروه ب'),
                           (4, 'نامشخص'), ]
Type_of_disease_list = [
    (1, 'عمومی'),
    (2, 'اعصاب و روان'),
    (3, 'ارتوپدی'),
    (4, 'خون و انکولوژی'),
    (5, 'چشم و عوارض بینائی'),
    (6, 'ریه و قفسه صدری'),
    (7, 'پوست و بافت های زیر پوست'),
    (8, 'دستگاه گوارش و جراحی عمومی'),
    (9, 'جراحی مغز و اعصاب'),
    (10, 'دستگاه ادراری و تناسلی'),
    (11, 'داخلی مغز و اعصاب'),
    (12, 'غدد مترشحه داخلی'),
    (13, 'قلب و عروق'),
    (14, 'کمیسیون'),
    (15, 'عفونی'),
    (16, 'بیماریهای غدد مترشحه داخلی'),
    (17, 'آموزشگاه'),
]

Grade_list = [(1, 'زیر دیپلم'), (2, 'دیپلم'), (3, 'فوق دیپلم'), (4, 'لیسانس'), (5, 'فوق لیسانس'), (6, 'دکتری'),
              (7, 'نامشخص')]

Grade_precise_list = [
    (1, 'بیسواد'),
    (2, 'نهضت سواد آموزی'),
    (3, 'ابتدایی'),
    (4, 'راهنمایی'),
    (5, 'سیکل'),
    (6, 'دبیرستان'),
    (7, 'زیر دیپلم'),
    (8, 'دیپلم'),
    (9, 'فوق دیپلم'),
    (10, 'لیسانس'),
    (11, 'فوق لیسانس'),
    (12, 'دکتری'),
    (13, 'نامشخص')
]
Amriye_list = [(1, 'بله'), (2, 'خیر')]
Amriye_organization_lsit = [(1, 'test1'), (2, 'test2')]
battalion_group_list = []
g = battalion_group.objects.filter().all()
for item in g:
    battalion_group_list.append((item.id, item.name))


class CreatePaziresh(LoginRequiredMixin, View):
    template = 'soldiers/CreatePazireshForm.html'
    success_url = reverse_lazy('moarefi_be_gordan_va_sater')

    def get(self, request):
        form_soldiers = FormSoldiersCreate()

        form_soldiers.fields['Religion'].choices = Religion_list
        form_soldiers.fields['province_name'].choices = province_name_list
        form_soldiers.fields['marital_status'].choices = marital_status_list
        form_soldiers.fields['physical_condition'].choices = physical_condition_list
        form_soldiers.fields['Grade'].choices = Grade_list
        form_soldiers.fields['Grade_precise'].choices = Grade_precise_list
        form_soldiers.fields['Type_of_disease'].choices = Type_of_disease_list
        form_soldiers.fields['Amriye'].choices = Amriye_list
        form_soldiers.fields['Sufficiency_of_mobilization'].choices = Sufficiency_of_mobilization_list
        form_soldiers.fields['Sutter'].choices = Sutter_list
        form_soldiers.fields['attraction_of_the_organization'].choices = attraction_of_the_organization_list
        form_soldiers.fields['Reason_for_renewing_the_course'].choices = Reason_for_renewing_the_course_list
        form_soldiers.fields['Renewal_of_the_previous_period'].choices = Renewal_of_the_previous_period_list
        form_soldiers.fields['educational_level_of_the_system'].choices = educational_level_of_the_system_list
        form_soldiers.fields['Amriye_organization'].choices = Amriye_organization_lsit
        form_soldiers.fields['battalion_group'].choices = battalion_group_list
        cx = {'form': form_soldiers}
        return render(request, self.template, cx)

    def post(self, request):
        form_soldiers = FormSoldiersCreate(request.POST, request.FILES or None)
        form_soldiers.fields['Religion'].choices = Religion_list
        form_soldiers.fields['province_name'].choices = province_name_list
        form_soldiers.fields['marital_status'].choices = marital_status_list
        form_soldiers.fields['physical_condition'].choices = physical_condition_list
        form_soldiers.fields['Grade'].choices = Grade_list
        form_soldiers.fields['Grade_precise'].choices = Grade_precise_list
        form_soldiers.fields['Type_of_disease'].choices = Type_of_disease_list
        form_soldiers.fields['Amriye'].choices = Amriye_list
        form_soldiers.fields['Sufficiency_of_mobilization'].choices = Sufficiency_of_mobilization_list
        form_soldiers.fields['Sutter'].choices = Sutter_list
        form_soldiers.fields['attraction_of_the_organization'].choices = attraction_of_the_organization_list
        form_soldiers.fields['Reason_for_renewing_the_course'].choices = Reason_for_renewing_the_course_list
        form_soldiers.fields['Renewal_of_the_previous_period'].choices = Renewal_of_the_previous_period_list
        form_soldiers.fields['educational_level_of_the_system'].choices = educational_level_of_the_system_list
        form_soldiers.fields['Amriye_organization'].choices = Amriye_organization_lsit
        form_soldiers.fields['battalion_group'].choices = battalion_group_list

        if not form_soldiers.is_valid():
            cx = {'form': form_soldiers}
            return render(request, self.template, cx)
        # code = form_soldiers.cleaned_data['National_Code']
        # # s1 = sarbaz.objects.filter(National_Code=code).first()
        # # if s1 is None:
        # #     cx = {'form': form_soldiers}
        #     return render(request, self.template, cx)
        name = form_soldiers.cleaned_data['name']
        family = form_soldiers.cleaned_data['family']
        fathers_name = form_soldiers.cleaned_data['fathers_name']
        National_Code = form_soldiers.cleaned_data['National_Code']
        physical_condition_id = form_soldiers.cleaned_data['physical_condition']
        physical_condition = physical_condition_list[int(physical_condition_id) - 1][1]
        Type_of_disease_id = form_soldiers.cleaned_data['Type_of_disease']
        Type_of_disease = Type_of_disease_list[int(Type_of_disease_id) - 1][1]
        health_insurance_card = form_soldiers.cleaned_data['health_insurance_card']
        Grade_id = form_soldiers.cleaned_data['Grade']
        Grade = Grade_list[int(Grade_id) - 1][1]
        Grade_precise_id = form_soldiers.cleaned_data['Grade_precise']
        Grade_precise = Grade_precise_list[int(Grade_precise_id) - 1][1]
        educational_level_of_the_system = form_soldiers.cleaned_data['educational_level_of_the_system']
        Study_group = form_soldiers.cleaned_data['Study_group']
        marital_status_id = form_soldiers.cleaned_data['marital_status']
        marital_status = marital_status_list[int(marital_status_id) - 1][1]
        Religion_id = form_soldiers.cleaned_data['Religion']
        Religion = Religion_list[int(Religion_id) - 1][1]
        Date_of_birth = form_soldiers.cleaned_data['Date_of_birth']
        place_of_birth = form_soldiers.cleaned_data['place_of_birth']
        phone_number = form_soldiers.cleaned_data['phone_number']
        home_phone_number = form_soldiers.cleaned_data['home_phone_number']
        Date_of_dispatch = form_soldiers.cleaned_data['Date_of_dispatch']
        province_name_id = form_soldiers.cleaned_data['province_name']
        province_name = province_name_list[int(province_name_id) - 1][1]
        city_name = form_soldiers.cleaned_data['city_name']
        Address = form_soldiers.cleaned_data['Address']
        height = form_soldiers.cleaned_data['height']
        Weight = form_soldiers.cleaned_data['Weight']
        Renewal_of_the_previous_period = form_soldiers.cleaned_data['Renewal_of_the_previous_period']
        Course_renewal_date = form_soldiers.cleaned_data['Course_renewal_date']
        Amriye_id = form_soldiers.cleaned_data['Amriye']
        Amriye = Amriye_list[int(Amriye_id) - 1][1]
        Amriye_organization_id = form_soldiers.cleaned_data['Amriye_organization']
        Amriye_organization = Amriye_organization_lsit[int(Amriye_organization_id) - 1][1]
        Sufficiency_of_mobilization_id = form_soldiers.cleaned_data['Sufficiency_of_mobilization']
        Sufficiency_of_mobilization = Sufficiency_of_mobilization_list[int(Sufficiency_of_mobilization_id) - 1][1]
        Place_of_Issue = form_soldiers.cleaned_data['Place_of_Issue']
        Renewal_of_the_previous_period_code = form_soldiers.cleaned_data['Renewal_of_the_previous_period_code']
        attraction_of_the_organization_id = form_soldiers.cleaned_data['attraction_of_the_organization']
        attraction_of_the_organization = \
            attraction_of_the_organization_list[int(attraction_of_the_organization_id) - 1][1]
        Sutter_id = form_soldiers.cleaned_data['Sutter']
        Sutter = Sutter_list[int(Sutter_id) - 1][1]
        f_battalion_group = form_soldiers.cleaned_data['battalion_group']
        s = sarbaz()
        s.name = name
        s.family = family
        s.fathers_name = fathers_name
        s.National_Code = National_Code
        s.physical_condition = physical_condition
        s.Type_of_disease = Type_of_disease
        s.health_insurance_card = health_insurance_card
        s.Grade = s.Grade
        s.Grade_precise = Grade_precise
        s.educational_level_of_the_system = educational_level_of_the_system
        s.Study_group = Study_group
        s.marital_status = marital_status
        s.Religion = Religion
        s.Date_of_birth = Date_of_birth
        s.place_of_birth = place_of_birth
        s.phone_number = phone_number
        s.home_phone_number = home_phone_number
        s.Date_of_dispatch = Date_of_dispatch
        s.province_name = province_name
        s.city_name = city_name
        s.Address = Address
        s.Place_of_Issue = Place_of_Issue
        s.height = height
        s.Weight = Weight
        s.Renewal_of_the_previous_period = Renewal_of_the_previous_period
        s.Course_renewal_date = Course_renewal_date
        s.Renewal_of_the_previous_period_code = Renewal_of_the_previous_period_code
        if Amriye == 'بله':
            s.Amriye = True
        else:
            s.Amriye = False
        s.Amriye_organization = Amriye_organization
        if Sufficiency_of_mobilization == 'خیر':
            s.Sufficiency_of_mobilization = False
        else:
            s.Sufficiency_of_mobilization = True
        b = battalion_group.objects.filter(id=f_battalion_group).first()
        s.battalion_group = b
        s.Gordan = b.gordan
        s.attraction_of_the_organization = attraction_of_the_organization
        s.Sutter = Sutter
        s.Grade = Grade
        s.willing_to_learn = True

        c_s = sarbaz.objects.all()
        find_max_code_list = [0]
        for iteam in c_s:
            if iteam.code_paziresh is not None:
                find_max_code_list.append(int(iteam.code_paziresh))
        code_paziresh_max = max(find_max_code_list)
        s.code_paziresh = code_paziresh_max + 1
        s.tarikh_paziresh = jdatetime.datetime.now()
        code_gorhan_list = [0]
        c_s = sarbaz.objects.filter(battalion_group=s.battalion_group, Gordan=s.Gordan).all()
        for item in c_s:
            if item.code_gorhan is not None:
                code_gorhan_list.append(int(item.code_gorhan))
        s.code_gorhan = max(code_gorhan_list) + 1
        s.save()
        b.zarfiat = int(b.zarfiat) - 1
        b.save()
        return HttpResponseRedirect(reverse("moarefi_be_gordan_va_sater", kwargs={'pk': s.id}))


class MainViewSoldires(LoginRequiredMixin, View):
    def get(self, request):
        s = sarbaz.objects.filter().all()
        cx = {'s': s}
        return render(request, 'soldiers/MainViewSoldires.html', cx)
