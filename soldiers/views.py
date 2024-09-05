import jdatetime
import xlrd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from battalions.models import battalion, battalion_group
from soldiers.models import Soldier as sarbaz
from .forms import SarbazCodeMeli, FormSoldiers, FormSoldiersCreate, FormAddExelToDb, FormSoldiersUpdate
from saterapps.models import Sater
from django.db.models import Q

# all static data
battalion_group_list = [(99999999, '')]
g = battalion_group.objects.filter().all()
for item in g:
    battalion_group_list.append((item.id, F'گردان :{item.gordan.name} گروهان :{item.name}'))


def categorize_educational_level(level_id):
    if level_id in {14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 23, 24, 25,
                    37}:
        return 1, 'زیر دیپلم'
    elif level_id in {13, 25, 26}:
        return 2, 'دیپلم'
    elif level_id in {4, 5, 3, 6}:
        return 3, 'فوق دیپلم'
    elif level_id in {9, 10, 11, 12, 1, 40,41}:
        return 4, 'لیسانس'
    elif level_id in {7, 8}:
        return 5, 'فوق لیسانس'
    elif level_id in {2, 3}:
        return 6, 'دکتری'
    elif level_id == 0:
        return 7, 'نامشخص'
    else:
        return 7, 'نامشخص'


def map_educational_level_to_grade(level):
    grade_precise_mapping = {
        'بی‌سواد': [],
        'نهضت سواد آموزی': [],
        'ابتدایی': [14, 15, 16, 17, 18, 19, 27, 28, 29, 30, 31, 32, 33],
        'راهنمایی': [20, 21, 22, 34, 35, 36],
        'سیکل': [],
        'دبیرستان': [23, 24, 25, 37, 38, 39],
        'زیر دیپلم': [],
        'دیپلم': [13, 26],
        'فوق دیپلم': [4, 5, 6],
        'لیسانس': [9, 10, 11, 12, 1, 40,41],
        'فوق لیسانس': [7, 8],
        'دکتری': [2, 3],
        'نامشخص': [0]
    }

    for grade_level, grade_name in Grade_precise_list:
        if level in grade_precise_mapping[grade_name]:
            return grade_level, grade_name

    return None


grade_precise_mapping = {
    'بی‌سواد': [],
    'نهضت سواد آموزی': [],
    'ابتدایی': [14, 15, 16, 17, 18, 19, 27, 28, 29, 30, 31, 32, 33],
    'راهنمایی': [20, 21, 22, 34, 35, 36],
    'سیکل': [],
    'دبیرستان': [23, 24, 25, 37, 38, 39],
    'زیر دیپلم': [],
    'دیپلم': [13, 26],
    'فوق دیپلم': [4, 5, 6],
    'لیسانس': [9, 10, 11, 12, 1, 40,41],
    'فوق لیسانس': [7, 8],
    'دکتری': [2, 3],
    'نامشخص': [0, ]
}

province_name_list = [
    (0, 'نامشخص'),
    (1, 'مازندران'),
    (3, 'خراسان رضوی'),
    (4, 'خراسان جنوبی'),
    (5, 'خراسان شمالی'),
    (6, 'گلستان'),
    (7, 'گیلان'),
    (8, 'تهران'),
    (9, 'سمنان'),
    (10, 'البرز'),
    (11, 'یزد'),
    (12, 'هرمزگان'),
    (13, 'کردستان'),
    (14, 'ایلام'),
    (15, 'همدان'),
    (16, 'زنجان'),
    (17, 'کردستان'),
    (18, 'کرمان'),
    (19, 'لرستان'),
    (20, 'اردبیل'),
    (21, 'مرکزی'),
    (22, 'سیستان و بلوچستان'),
    (23, 'آذربایجان غربی'),
    (24, 'قزوین'),
    (25, 'اصفهان'),
    (26, 'آذربایجان شرقی'),
    (27, 'قم'),
    (28, 'کهگیلویه و بویراحمد'),
    (29, 'فارس'),
    (30, 'چهارمحال و بختیاری'),
    (31, 'کرمانشاه'),
    (32, 'خوزستان'),
]
educational_level_of_the_system_list = [
    (0, "نامشخص"),
    (1, "حوزوی سطح یو اهل سنت"),
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
    (14, "پایه یکم"),
    (15, "پایه دوم"),
    (16, "پایه سوم"),
    (17, "پایه چهارم"),
    (18, "پایه پنجم"),
    (19, "پایه ششم"),
    (20, "پایه هفتم"),
    (21, "پایه هشتم"),
    (22, "پایه نهم"),
    (23, "پایه دهم"),
    (24, "پایه یازدهم"),
    (25, "پایه دوازدهم"),
    (26, "پیش دانشگاهی"),
    (27, "اول ابتدایی"),
    (29, "دوم ابتدایی"),
    (30, "سوم ابتدایی"),
    (31, "چهارم ابتدایی"),
    (32, "پنجم ابتدایی"),
    (33, "ششم ابتدایی"),
    (34, "اول راهنمایی"),
    (35, "دوم راهنمایی"),
    (36, "سوم راهنمایی"),
    (37, "اول دبیرستان"),
    (38, "دوم دبیرستان"),
    (39, "سوم دبیرستان"),
    (40, "حوزوی سطح ىو اهل سنت"),
    (41, 'لیسانس پزشکی ناپیوسته'),
]

Renewal_of_the_previous_period_list = [(0, ""), (1, 'المهدی'), (2, 'شیراز')]
Reason_for_renewing_the_course_list = [(0, ''), (1, 'کمیسیون پزشکی'), (2, 'فرار'), (3, 'تجدید دوره'),
                                       (4, 'انضباطی'),
                                       (5, 'نامشخص')]
attraction_of_the_organization_list = [(1, 'هیچکدام'), (2, 'جذبی سپاه و مامور'), (3, 'جذبی نیروی زمینی'), ]
Sutter_list = [(0, 'نامشخص'), (1, 'مجوز دارد'), (2, 'نیاز به بررسی'), (3, 'مجوز ندارد')]
Sufficiency_of_mobilization_list = [(1, 'خیر'), (2, 'بله')]
marital_status_list = [(1, 'مجرد'), (2, 'متاهل'), (3, 'نامشخص')]
Religion_list = [(1, 'شیعه'), (2, 'اهل تسنن'), (3, 'نامشخص')]
physical_condition_list = [(1, 'سالم'), (2, 'معاف از رزم'), (3, 'گروه ب'), (4, 'معاف+گروه ب'),
                           (0, 'نامشخص'), ]
Type_of_disease_list = [
    (1, "نامشخص"),
    (2, 'سالم'),
    (3, 'عمومی'),
    (4, 'اعصاب و روان'),
    (5, 'ارتوپدی'),
    (6, 'خون و انکولوژی'),
    (7, 'چشم و عوارض بینایی'),
    (8, 'ریه و قفسه صدری'),
    (9, 'پوست و بافت‌های زیر پوست'),
    (10, 'دستگاه گوارش و جراحی عمومی'),
    (11, 'جراحی مغز و اعصاب'),
    (12, 'دستگاه ادراری و تناسلی'),
    (13, 'داخلی مغز و اعصاب'),
    (14, 'غدد مترشحه داخلی'),
    (15, 'قلب و عروق'),
    (16, 'کمیسیون'),
    (17, 'عفونی'),
    (18, 'بیماری‌های غدد مترشحه داخلی'),
    (19, 'آموزشگاه')
]

Grade_list = [
    (1, 'زیر دیپلم'),
    (2, 'دیپلم'),
    (3, 'فوق دیپلم'),
    (4, 'لیسانس'),
    (5, 'فوق لیسانس'),
    (6, 'دکتری'),
    (7, 'نامشخص')
]

Grade_precise_list = [
    (1, 'بی‌سواد'),
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
    (13, 'نامشخص'),
]

Amriye_list = [(1, 'بله'), (2, 'خیر')]
Amriye_organization_lsit = [(0, ''), (1, 'test1'), (2, 'test2')]


def get_id_of_list(ls, oj):
    for iteam in ls:
        if iteam[1] == str(oj):
            return iteam[0]


# end static data


def paziresh_code_meli(request, *args, **kwargs):
    sarbaz_code_meli = SarbazCodeMeli(request.POST or None)
    if sarbaz_code_meli.is_valid():
        code_meli = sarbaz_code_meli.cleaned_data.get('code_meli')
        return HttpResponseRedirect(reverse("get_sarbaz", args=[code_meli]))

    return render(request, 'soldiers/paziresh_idcode_view.html', context={'SarbazCodeMeli': sarbaz_code_meli})


class sabte_paziresh(LoginRequiredMixin, View):
    template = 'soldiers/sabte_paziresh_view.html'

    def get(self, request, pk):
        soldire = sarbaz.objects.filter(National_Code=pk).first()
        if soldire is None:
            cx = {}
            return render(request, self.template, cx)
        form_soldiers = FormSoldiers()
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

        # initial
        form_soldiers.initial['name'] = soldire.name
        form_soldiers.initial['family'] = soldire.family
        form_soldiers.initial['fathers_name'] = soldire.fathers_name
        form_soldiers.initial['National_Code'] = soldire.National_Code
        form_soldiers.initial['physical_condition'] = get_id_of_list(physical_condition_list,
                                                                     soldire.physical_condition)
        form_soldiers.initial['Type_of_disease'] = get_id_of_list(Type_of_disease_list, soldire.Type_of_disease)
        form_soldiers.initial['health_insurance_card'] = soldire.health_insurance_card
        form_soldiers.initial['Relative_to_inclusive'] = soldire.Relative_to_inclusive
        form_soldiers.initial['Relative_to_inclusive_number'] = soldire.Relative_to_inclusive_number
        grade = 7
        for iteam in Grade_list:
            if iteam[1] == soldire.Grade:
                grade = iteam[0]
        t_grade = 0

        grade_p = 0
        for iteam in Grade_precise_list:
            if iteam[1] == soldire.Grade_precise:
                grade_p = iteam[0]
        form_soldiers.initial['Grade_precise'] = grade_p

        form_soldiers.initial['educational_level_of_the_system'] = ''
        for elots in educational_level_of_the_system_list:
            if elots[1].replace(" ", "").replace("\u200c", "").replace('ي',
                                                                       'ی') == soldire.educational_level_of_the_system.replace(
                " ", "").replace("\u200c", "").replace('ي', 'ی'):
                form_soldiers.initial['Grade'] = (categorize_educational_level(elots[0]))[0]
                form_soldiers.initial['educational_level_of_the_system'] = elots[0]
                t_grade = (categorize_educational_level(elots[0]))[0]

        form_soldiers.initial['Study_group'] = soldire.Study_group
        if soldire.marital_status == 'مجرد':
            form_soldiers.initial['marital_status'] = 1
        elif soldire.marital_status == 'متاهل':
            form_soldiers.initial['marital_status'] = 2
        else:
            form_soldiers.initial['marital_status'] = 3
        if soldire.Religion == "شیعه":
            form_soldiers.initial['Religion'] = 1
        elif soldire.Religion == "اهل تسنن":
            form_soldiers.initial['Religion'] = 2
        else:
            form_soldiers.initial['Religion'] = 3

        form_soldiers.initial['Religion'] = get_id_of_list(Religion_list, soldire.Religion)
        form_soldiers.initial['Date_of_birth'] = soldire.Date_of_birth
        form_soldiers.initial['place_of_birth'] = soldire.place_of_birth
        form_soldiers.initial['phone_number'] = soldire.phone_number
        form_soldiers.initial['home_phone_number'] = soldire.home_phone_number
        form_soldiers.initial['Date_of_dispatch'] = soldire.Date_of_dispatch
        province_name = 0
        for p in province_name_list:
            if p[1] == soldire.province_name:
                province_name = p[0]
        form_soldiers.initial['province_name'] = province_name
        form_soldiers.initial['city_name'] = soldire.city_name
        form_soldiers.initial['Address'] = soldire.Address
        form_soldiers.initial['Place_of_Issue'] = soldire.Place_of_Issue
        form_soldiers.initial['height'] = soldire.height
        form_soldiers.initial['Weight'] = soldire.Weight
        form_soldiers.initial['Renewal_of_the_previous_period'] = get_id_of_list(Renewal_of_the_previous_period_list,
                                                                                 soldire.Renewal_of_the_previous_period)
        form_soldiers.initial['Course_renewal_date'] = soldire.Course_renewal_date
        form_soldiers.initial['Reason_for_renewing_the_course'] = get_id_of_list(Reason_for_renewing_the_course_list,
                                                                                 soldire.Reason_for_renewing_the_course)
        form_soldiers.initial['Renewal_of_the_previous_period_code'] = soldire.Renewal_of_the_previous_period_code
        if soldire.Amriye is False:
            form_soldiers.initial['Amriye'] = 2
        else:
            form_soldiers.initial['Amriye'] = 1
        form_soldiers.initial['Amriye_organization'] = get_id_of_list(Amriye_organization_lsit,
                                                                      soldire.Amriye_organization)
        form_soldiers.initial['Sufficiency_of_mobilization'] = get_id_of_list(Sufficiency_of_mobilization_list,
                                                                              soldire.Sufficiency_of_mobilization)
        form_soldiers.initial['attraction_of_the_organization'] = get_id_of_list(attraction_of_the_organization_list,
                                                                                 soldire.attraction_of_the_organization)
        if soldire.Sutter == 'مجوز دارد':
            form_soldiers.initial['Sutter'] = 1
        elif soldire.Sutter == 'نیاز به بررسی':
            form_soldiers.initial['Sutter'] = 2
        elif soldire.Sutter == 'مجوز ندارد':
            form_soldiers.initial['Sutter'] = 3
        else:
            form_soldiers.initial['Sutter'] = 0
        op = t_grade
        zirediplom = False
        diplom = False
        ofghdiplom = False
        lisans = False
        ofghlisans = False
        doctra = False
        shie = False
        ahle_tasnon = False
        q_of_edu = []
        q_of_Religion = []
        if op == 1:
            zirediplom = True
            q_of_edu.append(Q(zirediplom=zirediplom))
        if op == 2:
            diplom = True
            q_of_edu.append(Q(diplom=diplom))
        if op == 3:
            ofghdiplom = True
            q_of_edu.append(Q(ofghdiplom=ofghdiplom))
        if op == 4:
            lisans = True
            q_of_edu.append(Q(lisans=lisans))
        if op == 5:
            ofghlisans = True
            q_of_edu.append(Q(ofghlisans=ofghlisans))
        if op == 6:
            doctra = True
            q_of_edu.append(Q(doctra=doctra))

        if soldire.Religion == "شیعه":
            shie = True
            q_of_Religion.append(Q(shie=shie))
        if soldire.Religion == "اهل تسنن":
            ahle_tasnon = True
            q_of_Religion.append(Q(ahle_tasnon=ahle_tasnon))
        pc = 0
        for iteam in physical_condition_list:
            if iteam[1] == soldire.physical_condition:
                pc = iteam[0]
        salemm = False
        moafazrazm = False
        gorehbe = False
        moafazrazm_gorehbe = False
        q_of_pc = []
        if pc == 1:
            salemm = True
            q_of_pc.append(Q(salemm=salemm))
        if pc == 2:
            moafazrazm = True
            q_of_pc.append(Q(moafazrazm=moafazrazm))
        if pc == 3:
            gorehbe = True
            q_of_pc.append(Q(gorehbe=gorehbe))
        if pc == 4:
            moafazrazm_gorehbe = True
            q_of_pc.append(Q(moafazrazm_gorehbe=moafazrazm_gorehbe))
        bg = battalion_group.objects.filter(takmilzarmit=False).all()
        bgl = bg.filter(q_of_edu[0],
                        (q_of_Religion[0]), (q_of_pc[0])).order_by('gordan__order').first()
        if bgl is None:
            form_soldiers.initial['battalion_group'] = 0
        else:
            form_soldiers.initial['battalion_group'] = bgl.pk

        cx = {'form': form_soldiers}
        return render(request, self.template, cx)

    def post(self, request, pk):

        soldire = sarbaz.objects.filter(National_Code=pk).first()
        if soldire is None:
            cx = {}
            return render(request, self.template, cx)
        form_soldiers = FormSoldiers(request.POST or None)
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

        # initial
        form_soldiers.initial['name'] = soldire.name
        form_soldiers.initial['family'] = soldire.family
        form_soldiers.initial['fathers_name'] = soldire.fathers_name
        form_soldiers.initial['National_Code'] = soldire.National_Code
        form_soldiers.initial['physical_condition'] = soldire.physical_condition
        form_soldiers.initial['Type_of_disease'] = soldire.Type_of_disease
        form_soldiers.initial['health_insurance_card'] = soldire.health_insurance_card
        form_soldiers.initial['Relative_to_inclusive'] = soldire.Relative_to_inclusive
        form_soldiers.initial['Relative_to_inclusive_number'] = soldire.Relative_to_inclusive_number
        grade = 7
        for iteam in Grade_list:
            if iteam[1] == soldire.Grade:
                grade = iteam[0]
        t_grade = 0

        grade_p = 0
        for iteam in Grade_precise_list:
            if iteam[1] == soldire.Grade_precise:
                grade_p = iteam[0]
        form_soldiers.initial['Grade_precise'] = grade_p

        form_soldiers.initial['educational_level_of_the_system'] = ''
        for elots in educational_level_of_the_system_list:
            if elots[1].replace(" ", "").replace("\u200c", "").replace('ي',
                                                                       'ی') == soldire.educational_level_of_the_system.replace(
                " ", "").replace("\u200c", "").replace('ي', 'ی'):
                form_soldiers.initial['Grade'] = (categorize_educational_level(elots[0]))[0]
                form_soldiers.initial['educational_level_of_the_system'] = elots[0]
                t_grade = (categorize_educational_level(elots[0]))[0]

        form_soldiers.initial['Study_group'] = soldire.Study_group
        if soldire.marital_status == 'مجرد':
            form_soldiers.initial['marital_status'] = 1
        elif soldire.marital_status == 'متاهل':
            form_soldiers.initial['marital_status'] = 2
        else:
            form_soldiers.initial['marital_status'] = 3
        if soldire.Religion == "شیعه":
            form_soldiers.initial['Religion'] = 1
        elif soldire.Religion == "اهل تسنن":
            form_soldiers.initial['Religion'] = 2
        else:
            form_soldiers.initial['Religion'] = 3

        form_soldiers.initial['Religion'] = soldire.Religion
        form_soldiers.initial['Date_of_birth'] = soldire.Date_of_birth
        form_soldiers.initial['place_of_birth'] = soldire.place_of_birth
        form_soldiers.initial['phone_number'] = soldire.phone_number
        form_soldiers.initial['home_phone_number'] = soldire.home_phone_number
        form_soldiers.initial['Date_of_dispatch'] = soldire.Date_of_dispatch
        province_name = 0
        for p in province_name_list:
            if p[1] == soldire.province_name:
                province_name = p[0]
        form_soldiers.initial['province_name'] = province_name
        form_soldiers.initial['city_name'] = soldire.city_name
        form_soldiers.initial['Address'] = soldire.Address
        form_soldiers.initial['Place_of_Issue'] = soldire.Place_of_Issue
        form_soldiers.initial['height'] = soldire.height
        form_soldiers.initial['Weight'] = soldire.Weight
        form_soldiers.initial['Renewal_of_the_previous_period'] = soldire.Renewal_of_the_previous_period
        form_soldiers.initial['Course_renewal_date'] = soldire.Course_renewal_date
        form_soldiers.initial['Reason_for_renewing_the_course'] = soldire.Reason_for_renewing_the_course
        form_soldiers.initial['Renewal_of_the_previous_period_code'] = soldire.Renewal_of_the_previous_period_code
        if soldire.Amriye is False:
            form_soldiers.initial['Amriye'] = 2
        else:
            form_soldiers.initial['Amriye'] = 1
        form_soldiers.initial['Amriye_organization'] = soldire.Amriye_organization
        form_soldiers.initial['Sufficiency_of_mobilization'] = soldire.Sufficiency_of_mobilization
        form_soldiers.initial['attraction_of_the_organization'] = soldire.attraction_of_the_organization
        if soldire.Sutter == 'مجوز دارد':
            form_soldiers.initial['Sutter'] = 1
        elif soldire.Sutter == 'نیاز به بررسی':
            form_soldiers.initial['Sutter'] = 2
        elif soldire.Sutter == 'مجوز ندارد':
            form_soldiers.initial['Sutter'] = 3
        else:
            form_soldiers.initial['Sutter'] = 0
        op = t_grade
        zirediplom = False
        diplom = False
        ofghdiplom = False
        lisans = False
        ofghlisans = False
        doctra = False
        shie = False
        ahle_tasnon = False
        q_of_edu = []
        q_of_Religion = []
        if op == 1:
            zirediplom = True
            q_of_edu.append(Q(zirediplom=zirediplom))
        if op == 2:
            diplom = True
            q_of_edu.append(Q(diplom=diplom))
        if op == 3:
            ofghdiplom = True
            q_of_edu.append(Q(ofghdiplom=ofghdiplom))
        if op == 4:
            lisans = True
            q_of_edu.append(Q(lisans=lisans))
        if op == 5:
            ofghlisans = True
            q_of_edu.append(Q(ofghlisans=ofghlisans))
        if op == 6:
            doctra = True
            q_of_edu.append(Q(doctra=doctra))

        if soldire.Religion == "شیعه":
            shie = True
            q_of_Religion.append(Q(shie=shie))
        if soldire.Religion == "اهل تسنن":
            ahle_tasnon = True
            q_of_Religion.append(Q(ahle_tasnon=ahle_tasnon))
        pc = 0
        for iteam in physical_condition_list:
            if iteam[1] == soldire.physical_condition:
                pc = iteam[0]
        salemm = False
        moafazrazm = False
        gorehbe = False
        moafazrazm_gorehbe = False
        q_of_pc = []
        if pc == 1:
            salemm = True
            q_of_pc.append(Q(salemm=salemm))
        if pc == 2:
            moafazrazm = True
            q_of_pc.append(Q(moafazrazm=moafazrazm))
        if pc == 3:
            gorehbe = True
            q_of_pc.append(Q(gorehbe=gorehbe))
        if pc == 4:
            moafazrazm_gorehbe = True
            q_of_pc.append(Q(moafazrazm_gorehbe=moafazrazm_gorehbe))
        bg = battalion_group.objects.filter(takmilzarmit=False).all()
        bgl = bg.filter(q_of_edu[0],
                        (q_of_Religion[0]), (q_of_pc[0])).order_by('gordan__order').first()
        if bgl is None:
            form_soldiers.initial['battalion_group'] = 0
        else:
            form_soldiers.initial['battalion_group'] = bgl.pk

        if not form_soldiers.is_valid():
            cx = {'form': form_soldiers}
            return render(request, self.template, cx)
        name = form_soldiers.cleaned_data['name']
        family = form_soldiers.cleaned_data['family']
        fathers_name = form_soldiers.cleaned_data['fathers_name']
        National_Code = form_soldiers.cleaned_data['National_Code']
        physical_condition_id = form_soldiers.cleaned_data['physical_condition']
        physical_condition = ""
        for iteam in physical_condition_list:
            if iteam[0] == int(physical_condition_id):
                physical_condition = iteam[1]
        Type_of_disease_id = form_soldiers.cleaned_data['Type_of_disease']
        Type_of_disease = ""
        for iteam in Type_of_disease_list:
            if iteam[0] == int(Type_of_disease_id):
                Type_of_disease = iteam[1]
        health_insurance_card = form_soldiers.cleaned_data['health_insurance_card']
        Grade_id = form_soldiers.cleaned_data['Grade']
        Grade = ""
        for iteam in Grade_list:
            if iteam[0] == int(Grade_id):
                Grade = iteam[1]
        Grade_precise_id = form_soldiers.cleaned_data['Grade_precise']
        Grade_precise = ""
        for iteam in Grade_precise_list:
            if iteam[0] == int(Grade_precise_id):
                Grade_precise = iteam[1]
        educational_level_of_the_system = form_soldiers.cleaned_data['educational_level_of_the_system']
        Study_group = form_soldiers.cleaned_data['Study_group']
        marital_status_id = form_soldiers.cleaned_data['marital_status']
        marital_status = ""
        for iteam in marital_status_list:
            if iteam[0] == int(marital_status_id):
                marital_status = iteam[1]
        Religion_id = form_soldiers.cleaned_data['Religion']
        Religion = ""
        for iteam in Religion_list:
            if iteam[0] == int(Religion_id):
                Religion = iteam[1]
        Date_of_birth = form_soldiers.cleaned_data['Date_of_birth']
        place_of_birth = form_soldiers.cleaned_data['place_of_birth']
        phone_number = form_soldiers.cleaned_data['phone_number']
        home_phone_number = form_soldiers.cleaned_data['home_phone_number']
        Date_of_dispatch = form_soldiers.cleaned_data['Date_of_dispatch']
        province_name_id = form_soldiers.cleaned_data['province_name']
        province_name = ""
        for iteam in province_name_list:
            if iteam[0] == int(province_name_id):
                province_name = iteam[1]
        city_name = form_soldiers.cleaned_data['city_name']
        Address = form_soldiers.cleaned_data['Address']
        height = form_soldiers.cleaned_data['height']
        Weight = form_soldiers.cleaned_data['Weight']
        Renewal_of_the_previous_period = form_soldiers.cleaned_data['Renewal_of_the_previous_period']
        Course_renewal_date = form_soldiers.cleaned_data['Course_renewal_date']
        Amriye_id = form_soldiers.cleaned_data['Amriye']
        Amriye = ""
        for iteam in Amriye_list:
            if iteam[0] == int(Amriye_id):
                Amriye = iteam[1]
        Amriye_organization_id = form_soldiers.cleaned_data['Amriye_organization']
        Amriye_organization = ""
        for iteam in Amriye_organization_lsit:
            if iteam[0] == int(Amriye_organization_id):
                Amriye_organization = iteam[1]
        Sufficiency_of_mobilization_id = form_soldiers.cleaned_data['Sufficiency_of_mobilization']
        Sufficiency_of_mobilization = ""
        for iteam in Sufficiency_of_mobilization_list:
            if iteam[0] == int(Sufficiency_of_mobilization_id):
                Sufficiency_of_mobilization = iteam[1]
        Place_of_Issue = form_soldiers.cleaned_data['Place_of_Issue']
        Renewal_of_the_previous_period_code = form_soldiers.cleaned_data['Renewal_of_the_previous_period_code']

        Relative_to_inclusive = form_soldiers.cleaned_data['Relative_to_inclusive']
        Relative_to_inclusive_number = form_soldiers.cleaned_data['Relative_to_inclusive']

        attraction_of_the_organization_id = form_soldiers.cleaned_data['attraction_of_the_organization']
        attraction_of_the_organization = ""
        for iteam in attraction_of_the_organization_list:
            if iteam[0] == int(attraction_of_the_organization_id):
                attraction_of_the_organization = iteam[1]
        Sutter_id = form_soldiers.cleaned_data['Sutter']
        Sutter = ""
        for iteam in Sutter_list:
            if iteam[0] == int(Sutter_id):
                Sutter = iteam[1]
        f_battalion_group = form_soldiers.cleaned_data['battalion_group']
        s = soldire
        s.name = name
        s.family = family
        s.Relative_to_inclusive = Relative_to_inclusive
        s.Relative_to_inclusive_number = Relative_to_inclusive_number
        count_all_acceptance = sarbaz.objects.filter(willing_to_learn=True).count()
        s.code_paziresh = int(count_all_acceptance) + 1
        s.acceptance_code = int(count_all_acceptance) + 1
        s.has_been_accepted = True
        s.fathers_name = fathers_name
        s.National_Code = National_Code
        s.physical_condition = physical_condition
        s.Type_of_disease = Type_of_disease
        s.health_insurance_card = health_insurance_card
        s.Grade = s.Grade
        s.Grade_precise = Grade_precise
        educational_level_of_the_system_name = ""
        for iteam in educational_level_of_the_system_list:
            if iteam[0] == int(educational_level_of_the_system):
                educational_level_of_the_system_name = iteam[1]
        s.educational_level_of_the_system = educational_level_of_the_system_name
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
        if Sufficiency_of_mobilization == "خیر":
            b = battalion_group.objects.filter(id=f_battalion_group).first()
            s.battalion_group = b
            s.Gordan = b.gordan
        s.attraction_of_the_organization = attraction_of_the_organization
        s.Sutter = Sutter
        s.Grade = Grade
        s.willing_to_learn = True

        c_s = sarbaz.objects.filter(IsCheckout=False, has_been_accepted=False, willing_to_learn=False).all()
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
        if Sufficiency_of_mobilization == "خیر":
            s.code_gorhan = max(code_gorhan_list) + 1
            b.zarfiat = int(b.zarfiat) - 1
            b.save()

        s.save()
        return HttpResponseRedirect(reverse("moarefi_be_gordan_va_sater", kwargs={'pk': s.id}))


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
        my_sarbaz = sarbaz.objects.filter(pk=pk).first()
        my_sater = Sater.objects.filter(sarbaz=my_sarbaz).first()
        if my_sater is None:
            my_sater = Sater()
        my_sater.sarbaz = my_sarbaz
        my_sater.date = jdatetime.datetime.now()
        my_sater.sub_user = request.user
        cx = {'sarbaz': my_sarbaz}
        if my_sarbaz.Sufficiency_of_mobilization == True:
            my_sater.sater_type = 'کفایت بسیج'
            my_sater.save()
            return render(request, 'soldiers/sater_kefaytbasij.html', cx)
        else:
            if my_sarbaz.Amriye == True:
                my_sater.sater_type = 'امریه'
                my_sater.save()
                return render(request, 'soldiers/sater_amriye.html', cx)
        my_sater.sater_type = 'عادلی'
        my_sater.save()
        return render(request, 'soldiers/sater_adi_page.html', cx)


class moarefibegordan(LoginRequiredMixin, View):

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(pk=pk).first()
        cx = {'sarbaz': my_sarbaz}
        return render(request, 'soldiers/pirint_moarefi_gordan.html', cx)


class CreatePaziresh(LoginRequiredMixin, View):
    template = 'soldiers/CreatePazireshForm.html'
    success_url = reverse_lazy('moarefi_be_gordan_va_sater')

    def get(self, request):
        battalion_group_list = [(99999999, '')]
        g = battalion_group.objects.filter().all()
        for item in g:
            battalion_group_list.append((item.id, F'گردان :{item.gordan.name} گروهان :{item.name}'))
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
        form_soldiers.initial['province_name'] = 32
        form_soldiers.initial['Religion'] = 0
        form_soldiers.initial['marital_status'] = 3
        form_soldiers.initial['physical_condition'] = 0
        form_soldiers.initial['Grade'] = 7
        form_soldiers.initial['Grade_precise'] = 13
        form_soldiers.initial['Type_of_disease'] = 0
        form_soldiers.initial['Amriye'] = 2
        form_soldiers.initial['Sufficiency_of_mobilization'] = 0
        cx = {'form': form_soldiers}
        return render(request, self.template, cx)

    def post(self, request):
        battalion_group_list = [(99999999, '')]
        g = battalion_group.objects.filter().all()
        for item in g:
            battalion_group_list.append((item.id, F'گردان :{item.gordan.name} گروهان :{item.name}'))
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

        name = form_soldiers.cleaned_data['name']
        family = form_soldiers.cleaned_data['family']
        fathers_name = form_soldiers.cleaned_data['fathers_name']
        National_Code = form_soldiers.cleaned_data['National_Code']
        physical_condition_id = form_soldiers.cleaned_data['physical_condition']
        physical_condition = ""
        for iteam in physical_condition_list:
            if iteam[0] == int(physical_condition_id):
                physical_condition = iteam[1]
        Type_of_disease_id = form_soldiers.cleaned_data['Type_of_disease']
        Type_of_disease = ""
        for iteam in Type_of_disease_list:
            if iteam[0] == int(Type_of_disease_id):
                Type_of_disease = iteam[1]
        health_insurance_card = form_soldiers.cleaned_data['health_insurance_card']
        Grade_id = form_soldiers.cleaned_data['Grade']
        Grade = ""
        for iteam in Grade_list:
            if iteam[0] == int(Grade_id):
                Grade = iteam[1]
        Grade_precise_id = form_soldiers.cleaned_data['Grade_precise']
        Grade_precise = ""
        for iteam in Grade_precise_list:
            if iteam[0] == int(Grade_precise_id):
                Grade_precise = iteam[1]
        educational_level_of_the_system = form_soldiers.cleaned_data['educational_level_of_the_system']
        Study_group = form_soldiers.cleaned_data['Study_group']
        marital_status_id = form_soldiers.cleaned_data['marital_status']
        marital_status = ""
        for iteam in marital_status_list:
            if iteam[0] == int(marital_status_id):
                marital_status = iteam[1]
        Religion_id = form_soldiers.cleaned_data['Religion']
        Religion = ""
        for iteam in Religion_list:
            if iteam[0] == int(Religion_id):
                Religion = iteam[1]
        Date_of_birth = form_soldiers.cleaned_data['Date_of_birth']
        place_of_birth = form_soldiers.cleaned_data['place_of_birth']
        phone_number = form_soldiers.cleaned_data['phone_number']
        home_phone_number = form_soldiers.cleaned_data['home_phone_number']
        Date_of_dispatch = form_soldiers.cleaned_data['Date_of_dispatch']
        province_name_id = form_soldiers.cleaned_data['province_name']
        province_name = province_name_list[int(province_name_id)][1]
        city_name = form_soldiers.cleaned_data['city_name']
        Address = form_soldiers.cleaned_data['Address']
        height = form_soldiers.cleaned_data['height']
        Weight = form_soldiers.cleaned_data['Weight']
        Renewal_of_the_previous_period = form_soldiers.cleaned_data['Renewal_of_the_previous_period']
        Course_renewal_date = form_soldiers.cleaned_data['Course_renewal_date']
        Amriye_id = form_soldiers.cleaned_data['Amriye']
        Amriye = ""
        for iteam in Amriye_list:
            if iteam[0] == int(Amriye_id):
                Amriye = iteam[1]
        Amriye_organization_id = form_soldiers.cleaned_data['Amriye_organization']
        Amriye_organization = ""
        for iteam in Amriye_organization_lsit:
            if iteam[0] == int(Amriye_organization_id):
                Amriye_organization = iteam[1]
        Sufficiency_of_mobilization_id = form_soldiers.cleaned_data['Sufficiency_of_mobilization']
        Sufficiency_of_mobilization = ""
        for iteam in Sufficiency_of_mobilization_list:
            if iteam[0] == int(Sufficiency_of_mobilization_id):
                Sufficiency_of_mobilization = iteam[1]
        Place_of_Issue = form_soldiers.cleaned_data['Place_of_Issue']
        Renewal_of_the_previous_period_code = form_soldiers.cleaned_data['Renewal_of_the_previous_period_code']
        attraction_of_the_organization_id = form_soldiers.cleaned_data['attraction_of_the_organization']
        attraction_of_the_organization = ""
        for iteam in attraction_of_the_organization_list:
            if iteam[0] == int(attraction_of_the_organization_id):
                attraction_of_the_organization = iteam[1]
        Sutter_id = form_soldiers.cleaned_data['Sutter']
        Sutter = ""
        for iteam in Sutter_list:
            if iteam[0] == int(Sutter_id):
                Sutter = iteam[1]
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
        s.has_been_accepted = True
        count_accepet_soldire = sarbaz.objects.filter(willing_to_learn=True).all().count()
        s.code_paziresh = int(count_accepet_soldire) + 1
        s.acceptance_code = int(count_accepet_soldire) + 1
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


class UpdatePazireshPage(LoginRequiredMixin, View):

    def get(self, request):
        form = SarbazCodeMeli()
        cx = {'form': form}
        return render(request, 'soldiers/updatepaziresh_idcode_page.html', cx)

    def post(self, request):
        form = SarbazCodeMeli(request.POST, request.FILES or None)
        if not form.is_valid():

            cx = {'from': form}
            return render(request, 'soldiers/updatepaziresh_idcode_page.html', cx)
        else:
            codemeli = form.cleaned_data['code_meli']
            return HttpResponseRedirect(reverse("updatePazireshpage", kwargs={'pk': int(codemeli)}))


def get_battalion_group(n):
    battalion_group_list = [(99999999, '')]
    g = battalion_group.objects.filter().all()
    for item in g:
        battalion_group_list.append((item.id, F'گردان :{item.gordan.name} گروهان :{item.name}'))
    for number, name in battalion_group_list:
        if name == n:
            return number
    return None


class UpdatePaziresh(LoginRequiredMixin, View):
    def get(self, request, pk):
        battalion_group_list = [(99999999, '')]
        g = battalion_group.objects.filter().all()
        for item in g:
            battalion_group_list.append((item.id, F'گردان :{item.gordan.name} گروهان :{item.name}'))
        sb = sarbaz.objects.filter(National_Code=pk).first()
        form_soldiers = FormSoldiersUpdate()
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

        # initial
        form_soldiers.initial['name'] = sb.name
        form_soldiers.initial['family'] = sb.family
        form_soldiers.initial['fathers_name'] = sb.fathers_name
        form_soldiers.initial['National_Code'] = sb.National_Code
        form_soldiers.initial['physical_condition'] = get_id_of_list(physical_condition_list, sb.physical_condition)
        form_soldiers.initial['Type_of_disease'] = get_id_of_list(Type_of_disease_list, sb.Type_of_disease)
        form_soldiers.initial['health_insurance_card'] = sb.health_insurance_card
        form_soldiers.initial['Grade'] = 7
        for iteam in Grade_list:
            if iteam[1] == sb.Grade:
                form_soldiers.initial['Grade'] = iteam[0]
        form_soldiers.initial['Grade_precise'] = 13
        for iteam in Grade_precise_list:
            if iteam[1] == sb.Grade_precise:
                form_soldiers.initial['Grade_precise'] = iteam[0]

        educational_level_of_the_system = ""
        for iteam in educational_level_of_the_system_list:
            if iteam[1] == sb.educational_level_of_the_system:
                educational_level_of_the_system = iteam[0]

        form_soldiers.initial['educational_level_of_the_system'] = educational_level_of_the_system
        form_soldiers.initial['Study_group'] = sb.Study_group
        form_soldiers.initial['marital_status'] = get_id_of_list(marital_status_list, sb.marital_status)
        form_soldiers.initial['Religion'] = get_id_of_list(Religion_list, sb.Religion)
        form_soldiers.initial['Date_of_birth'] = sb.Date_of_birth
        form_soldiers.initial['place_of_birth'] = sb.place_of_birth
        form_soldiers.initial['phone_number'] = sb.phone_number
        form_soldiers.initial['home_phone_number'] = sb.home_phone_number
        form_soldiers.initial['Date_of_dispatch'] = sb.Date_of_dispatch
        form_soldiers.initial['province_name'] = 0
        for iteam in province_name_list:
            if sb.province_name == iteam[1]:
                form_soldiers.initial['province_name'] = iteam[0]
        form_soldiers.initial['city_name'] = sb.city_name
        form_soldiers.initial['Address'] = sb.Address
        form_soldiers.initial['Place_of_Issue'] = sb.Place_of_Issue
        form_soldiers.initial['height'] = sb.height
        form_soldiers.initial['Weight'] = sb.Weight
        form_soldiers.initial['Renewal_of_the_previous_period'] = sb.Renewal_of_the_previous_period
        form_soldiers.initial['Course_renewal_date'] = sb.Course_renewal_date
        form_soldiers.initial['Reason_for_renewing_the_course'] = sb.Reason_for_renewing_the_course
        form_soldiers.initial['Renewal_of_the_previous_period_code'] = sb.Renewal_of_the_previous_period_code
        if sb.Amriye is True:
            form_soldiers.initial['Amriye'] = 1
        else:
            form_soldiers.initial['Amriye'] = 2
        form_soldiers.initial['Amriye_organization'] = get_id_of_list(Amriye_organization_lsit, sb.Amriye_organization)
        form_soldiers.initial['Sufficiency_of_mobilization'] = get_id_of_list(Sufficiency_of_mobilization_list,
                                                                              sb.Sufficiency_of_mobilization)
        form_soldiers.initial['attraction_of_the_organization'] = get_id_of_list(attraction_of_the_organization_list,
                                                                                 sb.attraction_of_the_organization)
        for iteam in Sutter_list:
            if iteam[1] == sb.Sutter:
                form_soldiers.initial['Sutter'] = iteam[0]
        form_soldiers.initial['Relative_to_inclusive'] = sb.Relative_to_inclusive
        form_soldiers.initial['Relative_to_inclusive_number'] = sb.Relative_to_inclusive_number
        if sb.battalion_group is not None:
            form_soldiers.initial['battalion_group'] = sb.battalion_group.pk
        else:
            form_soldiers.initial['battalion_group'] = 0
        cx = {'form': form_soldiers}
        return render(request, 'soldiers/UpdatePazireshForm.html', cx)

    def post(self, request, pk):
        battalion_group_list = [(99999999, '')]
        g = battalion_group.objects.filter().all()
        for item in g:
            battalion_group_list.append((item.id, F'گردان :{item.gordan.name} گروهان :{item.name}'))
        form = FormSoldiersUpdate(request.POST, request.FILES or None)
        sb = sarbaz.objects.filter(National_Code=pk).first()
        form.fields['Religion'].choices = Religion_list
        form.fields['province_name'].choices = province_name_list
        form.fields['marital_status'].choices = marital_status_list
        form.fields['physical_condition'].choices = physical_condition_list
        form.fields['Grade'].choices = Grade_list
        form.fields['Grade_precise'].choices = Grade_precise_list
        form.fields['Type_of_disease'].choices = Type_of_disease_list
        form.fields['Amriye'].choices = Amriye_list
        form.fields['Sufficiency_of_mobilization'].choices = Sufficiency_of_mobilization_list
        form.fields['Sutter'].choices = Sutter_list
        form.fields['attraction_of_the_organization'].choices = attraction_of_the_organization_list
        form.fields['Reason_for_renewing_the_course'].choices = Reason_for_renewing_the_course_list
        form.fields['Renewal_of_the_previous_period'].choices = Renewal_of_the_previous_period_list
        form.fields['educational_level_of_the_system'].choices = educational_level_of_the_system_list
        form.fields['Amriye_organization'].choices = Amriye_organization_lsit
        form.fields['battalion_group'].choices = battalion_group_list
        form.initial['name'] = sb.name
        form.initial['family'] = sb.family
        form.initial['fathers_name'] = sb.fathers_name
        form.initial['National_Code'] = sb.National_Code
        form.initial['physical_condition'] = sb.physical_condition
        form.initial['Type_of_disease'] = sb.Type_of_disease
        form.initial['health_insurance_card'] = sb.health_insurance_card
        form.initial['Grade'] = sb.Grade
        form.initial['Grade_precise'] = sb.Grade_precise
        form.initial['educational_level_of_the_system'] = sb.educational_level_of_the_system
        form.initial['Study_group'] = sb.Study_group
        form.initial['marital_status'] = sb.marital_status
        form.initial['Religion'] = sb.Religion
        form.initial['Date_of_birth'] = sb.Date_of_birth
        form.initial['place_of_birth'] = sb.place_of_birth
        form.initial['phone_number'] = sb.phone_number
        form.initial['home_phone_number'] = sb.home_phone_number
        form.initial['Date_of_dispatch'] = sb.Date_of_dispatch
        form.initial['Relative_to_inclusive'] = sb.Relative_to_inclusive
        form.initial['Relative_to_inclusive_number'] = sb.Relative_to_inclusive_number
        form.initial['province_name'] = 0
        for iteam in province_name_list:
            if sb.province_name == iteam[1]:
                form.initial['province_name'] = iteam[0]
        form.initial['city_name'] = sb.city_name
        form.initial['Address'] = sb.Address
        form.initial['Place_of_Issue'] = sb.Place_of_Issue
        form.initial['height'] = sb.height
        form.initial['Weight'] = sb.Weight
        form.initial['Renewal_of_the_previous_period'] = sb.Renewal_of_the_previous_period
        form.initial['Course_renewal_date'] = sb.Course_renewal_date
        form.initial['Reason_for_renewing_the_course'] = sb.Reason_for_renewing_the_course
        form.initial['Renewal_of_the_previous_period_code'] = sb.Renewal_of_the_previous_period_code
        if sb.Amriye is True:
            form.initial['Amriye'] = 1
        else:
            form.initial['Amriye'] = 2
        form.initial['Amriye_organization'] = sb.Amriye_organization
        form.initial['Sufficiency_of_mobilization'] = sb.Sufficiency_of_mobilization
        form.initial['attraction_of_the_organization'] = sb.attraction_of_the_organization
        form.initial['Sutter'] = sb.Sutter
        form.initial['battalion_group'] = sb.battalion_group.pk
        if not form.is_valid():
            cx = {'form': form}
            return render(request, 'soldiers/UpdatePazireshForm.html', cx)
        name = form.cleaned_data['name']
        family = form.cleaned_data['family']
        fathers_name = form.cleaned_data['fathers_name']
        National_Code = form.cleaned_data['National_Code']
        physical_condition_id = form.cleaned_data['physical_condition']
        physical_condition = ""
        for iteam in physical_condition_list:
            if iteam[0] == int(physical_condition_id):
                physical_condition = iteam[1]
        Type_of_disease_id = form.cleaned_data['Type_of_disease']
        Type_of_disease = ""
        for iteam in Type_of_disease_list:
            if iteam[0] == int(Type_of_disease_id):
                Type_of_disease = iteam[1]
        health_insurance_card = form.cleaned_data['health_insurance_card']
        Grade_id = form.cleaned_data['Grade']
        Grade = ""
        for iteam in Grade_list:
            if iteam[0] == int(Grade_id):
                Grade = iteam[1]
        Grade_precise_id = form.cleaned_data['Grade_precise']
        Grade_precise = ""
        for iteam in Grade_precise_list:
            if iteam[0] == int(Grade_precise_id):
                Grade_precise = iteam[1]
        educational_level_of_the_system = form.cleaned_data['educational_level_of_the_system']
        Study_group = form.cleaned_data['Study_group']
        marital_status_id = form.cleaned_data['marital_status']
        marital_status = ""
        for iteam in marital_status_list:
            if iteam[0] == int(marital_status_id):
                marital_status = iteam[1]
        Religion_id = form.cleaned_data['Religion']
        Religion = ""
        for iteam in Religion_list:
            if iteam[0] == int(Religion_id):
                Religion = iteam[1]
        Date_of_birth = form.cleaned_data['Date_of_birth']
        place_of_birth = form.cleaned_data['place_of_birth']
        phone_number = form.cleaned_data['phone_number']
        home_phone_number = form.cleaned_data['home_phone_number']
        Date_of_dispatch = form.cleaned_data['Date_of_dispatch']
        province_name_id = form.cleaned_data['province_name']
        province_name = ""
        for iteam in province_name_list:
            if iteam[0] == int(province_name_id):
                province_name = iteam[1]
        city_name = form.cleaned_data['city_name']
        Address = form.cleaned_data['Address']
        height = form.cleaned_data['height']
        Weight = form.cleaned_data['Weight']
        Renewal_of_the_previous_period = form.cleaned_data['Renewal_of_the_previous_period']
        Course_renewal_date = form.cleaned_data['Course_renewal_date']
        Amriye_id = form.cleaned_data['Amriye']
        Amriye = ""
        for iteam in Amriye_list:
            if iteam[0] == Amriye_id:
                Amriye = iteam[1]
        Amriye_organization_id = form.cleaned_data['Amriye_organization']
        Amriye_organization = ""
        for iteam in Amriye_organization_lsit:
            if iteam[0] == int(Amriye_organization_id):
                Amriye_organization = iteam[1]
        Sufficiency_of_mobilization_id = form.cleaned_data['Sufficiency_of_mobilization']
        Sufficiency_of_mobilization = ""
        for iteam in Sufficiency_of_mobilization_list:
            if iteam[0] == int(Sufficiency_of_mobilization_id):
                Sufficiency_of_mobilization = iteam[1]
        Place_of_Issue = form.cleaned_data['Place_of_Issue']
        Renewal_of_the_previous_period_code = form.cleaned_data['Renewal_of_the_previous_period_code']
        attraction_of_the_organization_id = form.cleaned_data['attraction_of_the_organization']
        attraction_of_the_organization = ""
        for iteam in attraction_of_the_organization_list:
            if iteam[0] == int(attraction_of_the_organization_id):
                attraction_of_the_organization = iteam[1]
        Sutter_id = form.cleaned_data['Sutter']
        Relative_to_inclusive = form.cleaned_data['Relative_to_inclusive']
        Relative_to_inclusive_number = form.cleaned_data['Relative_to_inclusive_number']
        Sutter = ""
        for iteam in Sutter_list:
            if iteam[0] == int(Sutter_id):
                Sutter = iteam[1]
        f_battalion_group = form.cleaned_data['battalion_group']
        sb.name = name
        sb.family = family
        sb.fathers_name = fathers_name
        sb.National_Code = National_Code
        sb.Relative_to_inclusive = Relative_to_inclusive
        sb.Relative_to_inclusive_number = Relative_to_inclusive_number
        sb.physical_condition = physical_condition
        sb.Type_of_disease = Type_of_disease
        sb.health_insurance_card = health_insurance_card
        sb.Grade = Grade
        sb.Grade_precise = Grade_precise
        sb.educational_level_of_the_system = educational_level_of_the_system
        print(educational_level_of_the_system)
        t_ed = 0
        for iteam in educational_level_of_the_system_list:
            if iteam[0] == int(educational_level_of_the_system):
                t_ed = iteam[1]

        sb.educational_level_of_the_system = t_ed
        sb.Study_group = Study_group
        sb.marital_status = marital_status
        sb.Religion = Religion
        sb.Date_of_birth = Date_of_birth
        sb.place_of_birth = place_of_birth
        sb.phone_number = phone_number
        sb.home_phone_number = home_phone_number
        sb.Date_of_dispatch = Date_of_dispatch
        sb.province_name = province_name
        sb.city_name = city_name
        sb.Address = Address
        sb.height = height
        sb.Weight = Weight
        sb.Renewal_of_the_previous_period = Renewal_of_the_previous_period
        sb.Course_renewal_date = Course_renewal_date
        if Amriye == 'بله':
            sb.Amriye = True
        else:
            sb.Amriye = False
        sb.Amriye_organization = Amriye_organization

        if Sufficiency_of_mobilization == 'خیر':
            sb.Sufficiency_of_mobilization = False
        else:
            sb.Sufficiency_of_mobilization = True
        sb.Place_of_Issue = Place_of_Issue
        sb.Renewal_of_the_previous_period_code = Renewal_of_the_previous_period_code
        sb.attraction_of_the_organization = attraction_of_the_organization
        sb.Sutter = Sutter
        if not sb.battalion_group == battalion_group.objects.filter(id=f_battalion_group).first().id:
            b_change = battalion_group.objects.filter(id=sb.battalion_group.id).first()
            b_change.zarfiat = int(b_change.zarfiat) + 1
            a_change = battalion_group.objects.filter(id=f_battalion_group).first()
            a_change.zarfiat = int(a_change.zarfiat) - 1
            sb.battalion_group = a_change
            sb.Gordan = a_change.gordan
            b_change.save()
            a_change.save()
        sb.save()
        return HttpResponseRedirect(reverse("moarefi_be_gordan_va_sater", kwargs={'pk': sb.id}))


class MainViewSoldires(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('table_search')
        if search is None:
            soldire = sarbaz.objects.filter().all()
            cx = {'s': soldire}
            return render(request, 'soldiers/MainViewSoldires.html', cx)
        if str(search).find('ی'):
            search_y = str(search).replace('ی', 'ي')
        else:
            search_y = search

        soldire = sarbaz.objects.filter(
            Q(name__icontains=search) | Q(family__icontains=search) | Q(name__icontains=search_y) | Q(
                family__icontains=search_y) |
            Q(National_Code__icontains=search) | Q(id__icontains=search)).all()
        cx = {'s': soldire}
        return render(request, 'soldiers/MainViewSoldires.html', cx)


class exel_add_to_db(View):
    def get(self, request):
        form = FormAddExelToDb()
        cx = {'form': form}
        return render(request, 'soldiers/AddExelToDb.html', cx)

    def post(self, request):
        form = FormAddExelToDb(request.POST, request.FILES or None)
        cx = {'form': form}

        if form.is_valid():
            exel = request.FILES['file']

            # Workbook را باز کنید
            workbook = xlrd.open_workbook(file_contents=exel.read())

            # شیت مورد نظر خود را انتخاب کنید (مثلاً شیت اول)
            sheet = workbook.sheet_by_index(0)

            # تعداد ردیف‌ها و ستون‌های شیت را بدست آورید
            num_rows = sheet.nrows
            num_cols = sheet.ncols
            # برای هر سطر
            for row_idx in range(1, num_rows):
                one_soldire_list = []
                soldire = sarbaz()
                for col_idx in range(num_cols):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell_value(row_idx, col_idx)
                    # مقدار دهی به لیست
                    if str(cell_value).find('ي'):
                        cell_value = str(cell_value).replace('ي', 'ی')
                    if str(cell_value).find('ك'):
                        cell_value = str(cell_value).replace('ك', 'ک')
                    if str(cell_value).find('ك'):
                        cell_value = str(cell_value).replace('ؤ', 'و')
                    one_soldire_list.append(cell_value)
                if not str(one_soldire_list[1]) == "null":
                    soldire.National_Code = str(one_soldire_list[1])
                if not str(one_soldire_list[1]) == "null":
                    soldire.name = str(one_soldire_list[2])
                if not str(one_soldire_list[1]) == "null":
                    soldire.family = str(one_soldire_list[3])
                if not str(one_soldire_list[1]) == "null":
                    soldire.fathers_name = str(one_soldire_list[4])
                if not str(one_soldire_list[1]) == "null":
                    soldire.place_of_birth = str(one_soldire_list[5])
                if not str(one_soldire_list[1]) == "null":
                    soldire.Date_of_birth = str(one_soldire_list[6])
                if not str(one_soldire_list[1]) == "null":
                    soldire.Place_of_Issue = str(one_soldire_list[7])
                if not str(one_soldire_list[1]) == "null":
                    soldire.Religion = str(one_soldire_list[8])
                if not str(one_soldire_list[1]) == "null":
                    soldire.educational_level_of_the_system = str(one_soldire_list[9])
                if not str(one_soldire_list[1]) == "null":
                    soldire.Study_group = str(one_soldire_list[10])
                if not str(one_soldire_list[1]) == "null":
                    soldire.Date_of_dispatch = str(one_soldire_list[11])
                if not str(one_soldire_list[1]) == "null":
                    soldire.height = str(one_soldire_list[12])
                if not str(one_soldire_list[1]) == "null":
                    soldire.Weight = str(one_soldire_list[13])
                if not str(one_soldire_list[1]) == "null":
                    soldire.province_name = str(one_soldire_list[14])
                if not str(one_soldire_list[1]) == "null":
                    soldire.city_name = str(one_soldire_list[15])
                if not str(one_soldire_list[1]) == "null":
                    soldire.Address = str(one_soldire_list[16])
                if not str(one_soldire_list[1]) == "null":
                    soldire.phone_number = str(one_soldire_list[17])
                if not str(one_soldire_list[1]) == "null":
                    soldire.home_phone_number = str(one_soldire_list[18])
                if not str(one_soldire_list[1]) == "null":
                    soldire.physical_condition = str(one_soldire_list[19])
                if not str(one_soldire_list[1]) == "null":
                    soldire.marital_status = str(one_soldire_list[20])
                soldire.willing_to_learn = False
                soldire.Sutter = "مجوز دارد"
                if not str(one_soldire_list[0]) == "null":
                    op = str(one_soldire_list[0])
                    if op == "پیام آور بهداشت":
                        soldire.Amriye = True
                    if op == "امریه دار":
                        soldire.Amriye = True
                temp = 0
                for i in educational_level_of_the_system_list:
                    if i[1].replace(" ", "").replace("\u200c", "") == one_soldire_list[9].replace(" ", "").replace(
                            "\u200c", ""):
                        temp = i[0]
                print(temp)
                print(categorize_educational_level(temp)[1])
                print(map_educational_level_to_grade(temp)[1])
                soldire.Grade = categorize_educational_level(temp)[1]
                soldire.Grade_precise = map_educational_level_to_grade(temp)[1]
                check_soldire = sarbaz.objects.filter(National_Code=str(one_soldire_list)).first()
                if check_soldire is None:
                    soldire.save()
        return render(request, 'soldiers/AddExelToDb.html', cx)


class exel_update_number(View):
    def get(self, request):
        form = FormAddExelToDb()
        cx = {'form': form}
        return render(request, 'soldiers/update_number.html', cx)

    def post(self, request):
        form = FormAddExelToDb(request.POST, request.FILES or None)
        cx = {'form': form}

        if form.is_valid():
            exel = request.FILES['file']

            # Workbook را باز کنید
            workbook = xlrd.open_workbook(file_contents=exel.read())

            # شیت مورد نظر خود را انتخاب کنید (مثلاً شیت اول)
            sheet = workbook.sheet_by_index(0)

            # تعداد ردیف‌ها و ستون‌های شیت را بدست آورید
            num_rows = sheet.nrows
            num_cols = sheet.ncols
            # برای هر سطر
            for row_idx in range(1, num_rows):
                my_list = []
                for col_idx in range(num_cols):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell_value(row_idx, col_idx)
                    # مقدار دهی به لیست
                    my_list.append(cell_value)
                code_meli = str(my_list[0])
                nesbat = str(my_list[1])
                shomre = str(my_list[2])
                find_soldire = sarbaz.objects.filter(National_Code__icontains=code_meli).first()
                my_list = []
                if find_soldire is not None:
                    find_soldire.Relative_to_inclusive = nesbat
                    find_soldire.Relative_to_inclusive_number = shomre
                    find_soldire.save()

        return render(request, 'soldiers/update_number.html', cx)


situation_list = [(1, 'عادی'), (2, 'پیام آور بهداشت'), (3, 'امریه دار'), (4, 'خاتم')]
