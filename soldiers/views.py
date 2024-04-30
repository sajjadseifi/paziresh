from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import resolve_url
from django.urls import reverse
from django.views import View
from soldiers.models import Soldier as sarbaz
from .forms import SarbazCodeMeli, FormSoldiers, FormSoldiersCreate


def paziresh_code_meli(request, *args, **kwargs):
    sarbaz_code_meli = SarbazCodeMeli(request.POST or None)
    if sarbaz_code_meli.is_valid():
        code_meli = sarbaz_code_meli.cleaned_data.get('code_meli')
        print(code_meli)
        return HttpResponseRedirect(reverse("get_sarbaz", args=[code_meli]))

    return render(request, 'soldiers/paziresh_idcode_view.html', context={'SarbazCodeMeli': sarbaz_code_meli})


class sabte_paziresh(LoginRequiredMixin, View):
    template = 'soldiers/sabte_paziresh_view.html'

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(National_Code=pk).first()
        cx = {'sarbaz': my_sarbaz}
        return render(request, self.template, cx)

    def post(self, request):
        cx = {}
        return render(request, self.template, cx)


class moarefi_be_gordan(LoginRequiredMixin, View):
    template = 'soldiers/moarefi_be_gordan.html'

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(National_Code=pk).first()
        cx = {'sarbaz': my_sarbaz}
        return render(request, self.template, cx)

    def post(self, request):
        cx = {}
        return render(request, self.template, cx)


class sater(LoginRequiredMixin, View):

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(National_Code=pk).first()
        cx = {'sarbaz': my_sarbaz}
        return render(request, 'soldiers/CreatePazireshForm.html', cx)
        # return render(request, 'soldiers/sater_adi_page.html', cx)


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


class CreatePaziresh(LoginRequiredMixin, View):
    template = 'soldiers/CreatePazireshForm.html'

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
        cx = {'form': form_soldiers}
        return render(request, self.template, cx)

    def post(self, request):
        form_soldiers = FormSoldiersCreate(request.POST, request.FILES or None)
        cx = {'form': form_soldiers}
        if not form_soldiers.is_valid():
            return render(request, self.template, cx)
        code = form_soldiers.cleaned_data['National_Code']
        s = sarbaz.objects.filter(National_Code=code).all()
        if s is not None:
            return render(request, self.template, cx)
        name = form_soldiers.cleaned_data['name']
        family = form_soldiers.cleaned_data['family']
        fathers_name = form_soldiers.cleaned_data['fathers_name']
        National_Code = form_soldiers.cleaned_data['National_Code']
        physical_condition_id = form_soldiers.cleaned_data['physical_condition']
        physical_condition = physical_condition_list[physical_condition_id - 1][1]
        Type_of_disease_id = form_soldiers.cleaned_data['Type_of_disease']
        Type_of_disease = Type_of_disease_list[Type_of_disease_id - 1][1]
        health_insurance_card = form_soldiers.cleaned_data['health_insurance_card']
        Grade_id = form_soldiers.cleaned_data['Grade']
        Grade = Grade_list[Grade_id - 1][1]
        Grade_precise_id = form_soldiers.cleaned_data['Grade_precise']
        Grade_precise = Grade_precise_list[Grade_precise_id - 1][1]
        educational_level_of_the_system = form_soldiers.cleaned_data['educational_level_of_the_system']
        Study_group = form_soldiers.cleaned_data['Study_group']
        marital_status_id = form_soldiers.cleaned_data['marital_status']
        marital_status = marital_status_list[marital_status_id - 1][1]
        Religion_id = form_soldiers.cleaned_data['Religion']
        Religion = Religion_list[Religion_id - 1][1]
        Date_of_birth = form_soldiers.cleaned_data['Date_of_birth']
        place_of_birth = form_soldiers.cleaned_data['place_of_birth']
        phone_number = form_soldiers.cleaned_data['phone_number']
        home_phone_number = form_soldiers.cleaned_data['home_phone_number']
        Date_of_dispatch = form_soldiers.cleaned_data['Date_of_dispatch']
        province_name_id = form_soldiers.cleaned_data['province_name']
        province_name = province_name_list[province_name_id - 1][1]
        city_name = form_soldiers.cleaned_data['city_name']
        Address = form_soldiers.cleaned_data['Address']
        height = form_soldiers.cleaned_data['height']
        Weight = form_soldiers.cleaned_data['Weight']
        Renewal_of_the_previous_period = form_soldiers.cleaned_data['Renewal_of_the_previous_period']
        Course_renewal_date = form_soldiers.cleaned_data['Course_renewal_date']
        Amriye_id = form_soldiers.cleaned_data['Amriye']
        Amriye = Amriye_list[Amriye_id - 1][1]
        Amriye_organization_id = form_soldiers.cleaned_data['Amriye_organization']
        Amriye_organization = 'هیج'
        Sufficiency_of_mobilization_id = form_soldiers.cleaned_data['Sufficiency_of_mobilization']
        Sufficiency_of_mobilization = Sufficiency_of_mobilization_list[Sufficiency_of_mobilization_id - 1][1]

        return render(request, self.template, cx)
