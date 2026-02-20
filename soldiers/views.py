import jdatetime
import xlrd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect,resolve_url
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from battalions.models import battalion, battalion_group
from soldiers.models import Soldier as sarbaz
from .forms import SarbazCodeMeli, FormSoldiers, FormSoldiersCreate, FormAddExelToDb, FormSoldiersUpdate,FormSaterGroup, FormMoarefiGroup, FormUpdatePazireshHazer, FormUpdatePazireshshode,FormKhatamChecked
from saterapps.models import Sater
from django.db.models import Q
from ensaniapp_settings.models import EnsaniSettings
from django.db import transaction, IntegrityError
import openpyxl

# all static data
def battalion_group_list_items():
    items = [(99999999, '')]
    g = battalion_group.objects.filter().order_by('gordan','name')
    
    for item in g:
        label = F'گردان {item.gordan.name}, گروهان {item.name}'
        if not item.is_active:
            label = f'{label} (   غیرفعال   )'
        elif item.takmilzarmit:
            label = f'{label} (   تکمیل ظرفیت   )'
        else:
            label = f'{label} (   {item.free_space} نفر خالی  )'
            
        items.append((item.id, label))

    return items
# تولید کد پذیرش یکتا
def generate_acceptance_code():
    code = sarbaz.objects.filter(has_been_accepted=True).count() + 1
    while sarbaz.objects.filter(acceptance_code=code).exists():
        code += 1
    return code
from .constants import *
from .utils import *


def get_id_of_list(ls, oj):
    for iteam in ls:
        if iteam[1] == str(oj):
            return iteam[0]


def get_name_of_list(ls, oj):
    for iteam in ls:
        if iteam[0] == int(oj):
            return iteam[1]


# end static data

@login_required
def paziresh_code_meli(request, *args, **kwargs):
    sarbaz_code_meli = SarbazCodeMeli(request.POST or None)
    if sarbaz_code_meli.is_valid():
        code_meli = sarbaz_code_meli.cleaned_data.get('code_meli')
        return HttpResponseRedirect(reverse("get_sarbaz", args=[code_meli]))

    soldiers = sarbaz.objects.filter(acceptance_code__isnull=False).order_by('-acceptance_code')[:50]
    saterForm = FormSaterGroup()
    saterForm.fields['type'].choices = [
        (1, "عادی"),
        (2, "کفایت دار بسیج"),
        (3, "امریه دار (مامور)"),
        (4, "کفایت دار خدمت قبلی")
    ]
    moarefiForm = FormMoarefiGroup()
    return render(request, 'soldiers/paziresh_idcode_view.html', context={
        'SarbazCodeMeli': sarbaz_code_meli,
        'soldiers':soldiers,
        'saterForm':saterForm,
        'moarefiForm':moarefiForm
    })


class sabte_paziresh(LoginRequiredMixin, View):
    template = 'soldiers/sabte_paziresh_view.html'

    def get(self, request, pk):

        soldire = sarbaz.objects.filter(National_Code=pk, has_been_accepted=False).first()
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
        form_soldiers.fields['battalion_group'].choices = battalion_group_list_items()

        form_soldiers.fields['status_type'].choices = Soldier.status_types_options()
        form_soldiers.initial['status_type'] = soldire.status_type
        form_soldiers.initial['date_improt_type'] = soldire.date_improt_type
        
        # initial
        form_soldiers.initial['name'] = soldire.name
        form_soldiers.initial['family'] = soldire.family
        form_soldiers.initial['fathers_name'] = soldire.fathers_name
        form_soldiers.initial['National_Code'] = soldire.National_Code
        form_soldiers.initial['physical_condition'] = get_id_of_list(physical_condition_list,soldire.physical_condition)
        form_soldiers.initial['Type_of_disease'] = get_id_of_list(Type_of_disease_list, soldire.Type_of_disease)
        form_soldiers.initial['health_insurance_card'] = soldire.health_insurance_card
        form_soldiers.initial['Relative_to_inclusive'] = soldire.Relative_to_inclusive
        form_soldiers.initial['Relative_to_inclusive_number'] = soldire.Relative_to_inclusive_number

        for idx,label in educational_level_of_the_system_list:
            if label == soldire.educational_level_of_the_system:
                form_soldiers.initial['educational_level_of_the_system'] = idx
                break
            
        grade = 7
        for iteam in Grade_list:
            if iteam[1] == soldire.Grade:
                grade = iteam[0]

        grade_p = 0
        for iteam in Grade_precise_list:
            if iteam[1] == soldire.Grade_precise:
                grade_p = iteam[0]
 
        form_soldiers.initial['Grade_precise'] = grade_p
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
        form_soldiers.initial['Renewal_of_the_previous_period'] = get_id_of_list(Renewal_of_the_previous_period_list,soldire.Renewal_of_the_previous_period)
        form_soldiers.initial['Course_renewal_date'] = soldire.Course_renewal_date
        form_soldiers.initial['Reason_for_renewing_the_course'] = get_id_of_list(Reason_for_renewing_the_course_list, soldire.Reason_for_renewing_the_course)
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
        op = grade
        q_of_edu = []
        q_of_Religion = []
        
        if op == 1:
            q_of_edu.append(Q(zirediplom=True))
        if op == 2:
            q_of_edu.append(Q(diplom=True))
        if op == 3:
            q_of_edu.append(Q(ofghdiplom=True))
        if op == 4:
            q_of_edu.append(Q(lisans=True))
        if op == 5:
            q_of_edu.append(Q(ofghlisans=True))
        if op == 6:
            q_of_edu.append(Q(doctra=True))

        if soldire.Religion == "شیعه":
            q_of_Religion.append(Q(shie=True))
        if soldire.Religion == "اهل تسنن":
            q_of_Religion.append(Q(ahle_tasnon=True))
            
        pc = 0
        for iteam in physical_condition_list:
            if iteam[1] == soldire.physical_condition:
                pc = iteam[0]

        q_of_pc = []
        if pc == 1:
            q_of_pc.append(Q(salemm=True))
        if pc == 2:
            q_of_pc.append(Q(moafazrazm=True))
        if pc == 3:
            q_of_pc.append(Q(gorehbe=True))
        if pc == 4:
            q_of_pc.append(Q(moafazrazm_gorehbe=True))
        
        bg = battalion_group.objects.filter(takmilzarmit=False).all()
        # وضعیت برگه اعزام
        query_json = dict({f'status_types_data__{soldire.status_type}':True})
        bg = bg.filter(q_of_edu[0], (q_of_Religion[0]), (q_of_pc[0]),Q(**query_json))
        
        bgl = bg.order_by('order').first()

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
        form_soldiers.fields['battalion_group'].choices = battalion_group_list_items()
        form_soldiers.fields['status_type'].choices = Soldier.status_types_options()
        form_soldiers.initial['status_type'] = soldire.status_type
        form_soldiers.initial['date_improt_type'] = soldire.date_improt_type

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
        form_soldiers.initial['educational_level_of_the_system'] = soldire.educational_level_of_the_system
        
        grade = 7
        
        for iteam in Grade_list:
            if iteam[1] == soldire.Grade:
                grade = iteam[0]
        grade_p = 0
        for iteam in Grade_precise_list:
            if iteam[1] == soldire.Grade_precise:
                grade_p = iteam[0]

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
        op = grade
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
        q_of_pc = []
        if pc == 1:
            q_of_pc.append(Q(salemm=True))
        if pc == 2:
            q_of_pc.append(Q(moafazrazm=True))
        if pc == 3:
            q_of_pc.append(Q(gorehbe=True))
        if pc == 4:
            q_of_pc.append(Q(moafazrazm_gorehbe=True))
            
        bg = battalion_group.objects.filter(takmilzarmit=False).all()
        
        bgl = bg.filter(q_of_edu[0],(q_of_Religion[0]), (q_of_pc[0])).order_by('gordan__order').first()
        
        if bgl is None:
            form_soldiers.initial['battalion_group'] = 0
        else:
            form_soldiers.initial['battalion_group'] = bgl.pk

        if not form_soldiers.is_valid() :
            return redirect(request.path)


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
        Renewal_of_the_previous_period_id = form_soldiers.cleaned_data['Renewal_of_the_previous_period']
        Renewal_of_the_previous_period = ""
        for iteam in Renewal_of_the_previous_period_list:
            if iteam[0] == int(Renewal_of_the_previous_period_id):
                Renewal_of_the_previous_period = iteam[1]
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
        Relative_to_inclusive_number = form_soldiers.cleaned_data['Relative_to_inclusive_number']

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
        status_type = form_soldiers.cleaned_data['status_type']
        date_improt_type = form_soldiers.cleaned_data['date_improt_type']
        while True:
            try:
                with transaction.atomic():
                    s = soldire
                    s.status_type = status_type
                    s.date_improt_type = date_improt_type
                    s.name = name
                    s.family = family
                    s.Relative_to_inclusive = Relative_to_inclusive
                    s.Relative_to_inclusive_number = Relative_to_inclusive_number
                    count_all_acceptance = sarbaz.objects.filter(has_been_accepted=True).count()
                    s.code_paziresh = int(count_all_acceptance) + 1
                    s.acceptance_code = generate_acceptance_code()
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
                        s.willing_to_learn = True
                        s.in_coures = True
                    else:
                        s.Sufficiency_of_mobilization = True
                        s.willing_to_learn = False
                    if Sufficiency_of_mobilization == "خیر":
                        b = battalion_group.objects.filter(id=f_battalion_group).first()
                        s.battalion_group = b
                        s.Gordan = b.gordan
                    s.attraction_of_the_organization = attraction_of_the_organization
                    s.Sutter = Sutter
                    s.Grade = Grade
                    c_s = sarbaz.objects.filter(has_been_accepted=True).all()
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
                        # b.zarfiat = int(b.zarfiat) - 1

                    s.save()

                    if Sufficiency_of_mobilization == "خیر":
                        if b.free_space < 1:
                            b.takmilzarmit = True
                        b.save()
                break  # اگر ذخیره موفق بود، از حلقه خارج شویم
            except IntegrityError:
                continue
        return HttpResponseRedirect(reverse("moarefi_be_gordan_va_sater", kwargs={'pk': s.id}))


class moarefi_be_gordan_va_sater(LoginRequiredMixin, View):
    template = 'soldiers/moarefi_be_gordan_va_sater.html'

    def get(self, request, pk):
        soldiers = sarbaz.objects.filter(acceptance_code__isnull=False).order_by('-acceptance_code')[:50]
        my_sarbaz = sarbaz.objects.filter(pk=pk).first()
        time = ""
        date = ""
        if my_sarbaz.tarikh_paziresh is not None:
            time = my_sarbaz.tarikh_paziresh.time()
            date = my_sarbaz.tarikh_paziresh.date()
        cx = {'sarbaz': my_sarbaz, 'time': time, 'date': date,'soldiers' : soldiers}
        return render(request, self.template, cx)

    def post(self, request, pk):
        soldiers = sarbaz.objects.filter(acceptance_code__isnull=False).order_by('-acceptance_code')[:6]
        
        cx = {'soldiers' : soldiers}
        return render(request, self.template, cx)


class sater(LoginRequiredMixin, View):

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(pk=pk).first()
        my_sater = Sater.objects.filter(sarbaz=my_sarbaz).first()
        en = EnsaniSettings.objects.filter().first()
        if my_sater is None:
            my_sater = Sater()
        my_sater.sarbaz = my_sarbaz
        my_sater.date = jdatetime.datetime.now()
        my_sater.sub_user = request.user
        cx = {'sarbaz': my_sarbaz, 'en': en}
        if my_sarbaz.Sufficiency_of_mobilization == True:
            my_sater.sater_type = 'کفایت بسیج'
            my_sater.save()
            return render(request, 'soldiers/sater_kefaytbasij.html', cx)

        elif my_sarbaz.Amriye == True:
            my_sater.sater_type = 'امریه'
            my_sater.save()
            return render(request, 'soldiers/sater_amriye.html', cx)
        if my_sarbaz.Previous_service_record == True:
            my_sater.sater_type = 'خدمت قبلی'
            my_sater.save()
            return render(request, 'soldiers/khedmat_ghabli.html', cx)
        else:
            my_sater.sater_type = 'عادلی'
            my_sater.save()
        return render(request, 'soldiers/sater_adi_page.html', cx)


class moarefibegordan(LoginRequiredMixin, View):

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(pk=pk).first()
        en = EnsaniSettings.objects.filter().first()
        cx = {'sarbaz': my_sarbaz, 'en': en}
        return render(request, 'soldiers/pirint_moarefi_gordan.html', cx)


class CreatePaziresh(LoginRequiredMixin, View):
    template = 'soldiers/CreatePazireshForm.html'
    success_url = reverse_lazy('moarefi_be_gordan_va_sater')

    def get(self, request):
        form_soldiers = FormSoldiersCreate()
        form_soldiers.fields['status_type'].choices = Soldier.status_types_options()
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
        form_soldiers.fields['battalion_group'].choices = battalion_group_list_items()
        form_soldiers.initial['province_name'] = 0
        form_soldiers.initial['Religion'] = 0
        form_soldiers.initial['marital_status'] = 3
        form_soldiers.initial['physical_condition'] = 0
        form_soldiers.initial['Grade'] = 7
        form_soldiers.initial['Grade_precise'] = 13
        form_soldiers.initial['Type_of_disease'] = 0
        form_soldiers.initial['Amriye'] = 2
        form_soldiers.initial['Sufficiency_of_mobilization'] = 0
        form_soldiers.initial['date_improt_type'] = 'دست نویس'
    
        cx = {'form': form_soldiers}
        return render(request, self.template, cx)

    def post(self, request):

        form_soldiers = FormSoldiersCreate(request.POST, request.FILES or None)
        form_soldiers.fields['status_type'].choices = Soldier.status_types_options()
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
        form_soldiers.fields['battalion_group'].choices = battalion_group_list_items()
        form_soldiers.initial['date_improt_type'] = 'دست نویس'
        
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
        educational_level_of_the_system_id = form_soldiers.cleaned_data['educational_level_of_the_system']
        educational_level_of_the_system = ""
        for iteam in educational_level_of_the_system_list:
            if iteam[0] == int(educational_level_of_the_system_id):
                educational_level_of_the_system = iteam[1]

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
        province_name = get_name_of_list(province_name_list, province_name_id)
        city_name = form_soldiers.cleaned_data['city_name']
        Address = form_soldiers.cleaned_data['Address']
        height = form_soldiers.cleaned_data['height']
        Weight = form_soldiers.cleaned_data['Weight']
        Renewal_of_the_previous_period_id = form_soldiers.cleaned_data['Renewal_of_the_previous_period']
        Renewal_of_the_previous_period = ""
        for iteam in Renewal_of_the_previous_period_list:
            if iteam[0] == int(Renewal_of_the_previous_period_id):
                Renewal_of_the_previous_period = iteam[1]
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
        Relative_to_inclusive = form_soldiers.cleaned_data['Relative_to_inclusive']
        Relative_to_inclusive_number = form_soldiers.cleaned_data['Relative_to_inclusive_number']
        f_battalion_group = form_soldiers.cleaned_data['battalion_group']

        status_type = form_soldiers.cleaned_data['status_type']
        date_improt_type = form_soldiers.cleaned_data['date_improt_type']

        while True:
            try:
                with transaction.atomic():
                    s = sarbaz()
                    s.status_type = status_type
                    s.date_improt_type = date_improt_type
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
                    s.Relative_to_inclusive = Relative_to_inclusive
                    s.Relative_to_inclusive_number = Relative_to_inclusive_number
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
                        s.willing_to_learn = True
                        s.in_coures = True
                    else:
                        s.Sufficiency_of_mobilization = True
                        s.willing_to_learn = False
                    b = battalion_group.objects.filter(id=f_battalion_group).first()
                    if b is not None:
                        s.battalion_group = b
                        s.Gordan = b.gordan
                    s.attraction_of_the_organization = attraction_of_the_organization
                    s.Sutter = Sutter
                    s.Grade = Grade
                    s.has_been_accepted = True
                    count_accepet_soldire = sarbaz.objects.filter(has_been_accepted=True).all().count()
                    s.code_paziresh = int(count_accepet_soldire) + 1
                    s.acceptance_code = generate_acceptance_code()
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
                            # b.zarfiat = int(b.zarfiat) - 1
                    s.save()
                    
                    if b.free_space < 1:
                        b.takmilzarmit = True
                    b.save()
                break  # اگر ذخیره موفق بود، از حلقه خارج شویم
            except IntegrityError:
                continue
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
        form_soldiers.fields['battalion_group'].choices = battalion_group_list_items()
        form_soldiers.fields['status_type'].choices = Soldier.status_types_options()

        # initial
        form_soldiers.initial['status_type'] = sb.status_type
        form_soldiers.initial['date_improt_type'] = sb.date_improt_type
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
        form_soldiers.initial['Renewal_of_the_previous_period'] = get_id_of_list(Renewal_of_the_previous_period_list,
                                                                                 sb.Renewal_of_the_previous_period)
        form_soldiers.initial['Course_renewal_date'] = sb.Course_renewal_date
        form_soldiers.initial['Reason_for_renewing_the_course'] = sb.Reason_for_renewing_the_course
        form_soldiers.initial['Renewal_of_the_previous_period_code'] = sb.Renewal_of_the_previous_period_code
        if sb.Amriye is True:
            form_soldiers.initial['Amriye'] = 1
        else:
            form_soldiers.initial['Amriye'] = 2
        form_soldiers.initial['Amriye_organization'] = get_id_of_list(Amriye_organization_lsit, sb.Amriye_organization)
        if sb.Sufficiency_of_mobilization == True:
            form_soldiers.initial['Sufficiency_of_mobilization'] = 2
        else:
            form_soldiers.initial['Sufficiency_of_mobilization'] = 1
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
        form = FormSoldiersUpdate(request.POST, request.FILES or None)
        sb = sarbaz.objects.filter(National_Code=pk).first()
        form.fields['status_type'].choices = Soldier.status_types_options()


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
        form.fields['battalion_group'].choices = battalion_group_list_items()
        
        form.initial['status_type'] = sb.status_type
        form.initial['date_improt_type'] = sb.date_improt_type
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
        if sb.battalion_group is not None:
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
        Renewal_of_the_previous_period_id = form.cleaned_data['Renewal_of_the_previous_period']
        Renewal_of_the_previous_period = ""
        for iteam in Renewal_of_the_previous_period_list:
            if iteam[0] == int(Renewal_of_the_previous_period_id):
                Renewal_of_the_previous_period = iteam[1]
        Course_renewal_date = form.cleaned_data['Course_renewal_date']
        Amriye_id = form.cleaned_data['Amriye']
        Amriye = ""
        for iteam in Amriye_list:
            if iteam[0] == int(Amriye_id):
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
        
        status_type = form.cleaned_data['status_type']
        date_improt_type = form.cleaned_data['date_improt_type']
        sb.status_type = status_type
        sb.date_improt_type = date_improt_type
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
            sb.willing_to_learn = True
            sb.in_coures = True
        else:
            sb.Sufficiency_of_mobilization = True
            sb.willing_to_learn = False
            sb.in_coures = False
        sb.Place_of_Issue = Place_of_Issue
        sb.Renewal_of_the_previous_period_code = Renewal_of_the_previous_period_code
        sb.attraction_of_the_organization = attraction_of_the_organization
        sb.Sutter = Sutter

        bt = battalion_group.objects.filter(id=f_battalion_group).filter().first()
        if bt is None:
            sb.Gordan = None
            sb.battalion_group = None
        else:
            sb.Gordan = bt.gordan
            sb.battalion_group = bt
        sb.Previous_service_record = False
        sb.save()
        return HttpResponseRedirect(reverse("moarefi_be_gordan_va_sater", kwargs={'pk': sb.id}))


class MainViewSoldires(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('table_search','')
        gordan = request.GET.get('gordan','')
        group = request.GET.get('group','')
        acceptance_status = request.GET.get('acceptance_status','')
        status_type = request.GET.get('status_type','')
        status_type = request.GET.get('status_type','')
        
        name = request.GET.get('name')
        family = request.GET.get('family')
        national_code = request.GET.get('national_code')
        acceptance_code = request.GET.get('acceptance_code')
            
        soldiers = sarbaz.objects.all()
        all_counts = soldiers.count() 
        
        
        if name:
            soldire = soldiers.filter(name__icontains=name)
        if family:
            soldire = soldiers.filter(family__icontains=family)
        if national_code:
            soldiers = soldiers.filter(National_Code__icontains=national_code)
        if acceptance_code:
            soldiers = soldiers.filter(acceptance_code=acceptance_code)
            
            
        if status_type:
            soldiers = soldiers.filter(status_type=status_type)

        if acceptance_status == 'acceptance':
            soldiers = soldiers.filter(has_been_accepted=True)
            
        if acceptance_status == 'no_acceptance':
            soldiers = soldiers.filter(has_been_accepted=False)
        if acceptance_status == 'system':
            soldiers = soldiers.filter(date_improt_type='سامانه',)
        if acceptance_status == 'system_acceptance':
            soldiers = soldiers.filter(date_improt_type='سامانه',has_been_accepted=True)
        if acceptance_status == 'system_no_acceptance':
            soldiers = soldiers.filter(date_improt_type='سامانه',has_been_accepted=False)
        if acceptance_status == 'manual':
            soldiers = soldiers.filter(date_improt_type='')
        
        if gordan == 'no':
            soldiers = soldiers.filter(Gordan__isnull=True)
        elif gordan:
            soldiers = soldiers.filter(Gordan=gordan)
        
        if group == 'no':
            soldiers = soldiers.filter(battalion_group__isnull=True)
        elif group:
            soldiers = soldiers.filter(battalion_group=group)

        gordans = battalion.objects.all()
        result_counts = soldiers.count() 

        cx = {
            # forms
            'acceptance_status_list':acceptance_status_list,
            'acceptance_status':acceptance_status,
            'search':search,
            'gordan':gordan,
            'group':group,
            'acceptance_status':acceptance_status,
            'status_type':status_type,
            'status_types':sarbaz.valid_status_types(),
            'unkhown_status_types':sarbaz.unkhown_status_types(),
            'gordans':gordans,
            # 
            'results': soldiers,
            'result_counts': result_counts,
            'all_counts':all_counts,
        }
        
        return render(request, 'soldiers/MainViewSoldires.html', cx)

from .models import Soldier
def generate_grade_temp(educational_level_of_the_system):
    temp = 0
    for i in educational_level_of_the_system_list:
        i1 = i[1].replace(" ", "").replace("\u200c", "")
        nv =  educational_level_of_the_system.replace(" ", "").replace("\u200c", "")
        if i1 == nv:
            temp = i[0]
            
    return temp

from ensani_statistics.utils import DASH_REGEX,normalization_persian,smart_separation

class exel_add_to_db(LoginRequiredMixin, View):
    def get(self, request):
        form = FormAddExelToDb()
        khatam_form = FormKhatamChecked()
        cx = {'form': form,'khatam_form':khatam_form}
        return render(request, 'soldiers/AddExelToDb.html', cx)

    def post(self, request):
        form = FormAddExelToDb(request.POST, request.FILES or None)
        khatam_form = FormKhatamChecked()
    
        cx = {'form': form,'khatam_form':khatam_form}
        updated_counts = 0
        add_count = 0
        skipped_count = 0
        if form.is_valid():
            exel = request.FILES['file']
            workbook = xlrd.open_workbook(file_contents=exel.read())
            # شیت مورد نظر خود را انتخاب کنید (مثلاً شیت اول)
            sheet = workbook.sheet_by_index(0)
            # تعداد ردیف‌ها و ستون‌های شیت را بدست آورید
            num_rows = sheet.nrows
            num_cols = sheet.ncols
            # برای هر سطر
            for row_idx in range(1, num_rows):
                # nc = str(one_soldire_list[1]).strip()
                # if action == 'new':
                #     exist_soldier = Soldier.objects.filter(National_Code=nc).first()
                #     if exist_soldier:
                #         continue
                
                one_soldire_list = []
                
                for col_idx in range(num_cols):
                    # # مقدار سلول را بخوانید
                    cell_value = sheet.cell_value(row_idx, col_idx)
                    cell_value = normalization_persian(cell_value)
                    # # مقدار دهی به لیست
                    # if str(cell_value).find('ي'):
                    #     cell_value = str(cell_value).replace('ي', 'ی')
                    # if str(cell_value).find('ك'):
                    #     cell_value = str(cell_value).replace('ك', 'ک')
                    # if str(cell_value).find('ك'):
                    #     cell_value = str(cell_value).replace('ؤ', 'و')
                    one_soldire_list.append(cell_value)
                
                has_national = not str(one_soldire_list[1]) == "null"
                check_soldire = sarbaz.objects.filter(National_Code=str(one_soldire_list[1])).first()
                if check_soldire:
                    if not form.cleaned_data['can_edit']:
                        skipped_count += 1
                        continue
                    soldire = check_soldire
                    updated_counts += 1
                else:
                    if not form.cleaned_data['can_add']:
                        skipped_count += 1
                        continue
                    add_count += 1
                    soldire = sarbaz()
                
                if has_national:
                    soldire.status_type = str(one_soldire_list[0]) # flexible types of soldiers       
                if has_national:
                    soldire.National_Code = str(one_soldire_list[1])
                if has_national:
                    soldire.name = str(one_soldire_list[2])
                if has_national:
                    soldire.family = str(one_soldire_list[3])
                if has_national:
                    soldire.fathers_name = str(one_soldire_list[4])
                if has_national:
                    soldire.place_of_birth = str(one_soldire_list[5])
                if has_national:
                    soldire.Date_of_birth = str(one_soldire_list[6])
                if has_national:
                    soldire.Place_of_Issue = str(one_soldire_list[7])
                if has_national:
                    soldire.Religion = str(one_soldire_list[8])
                if has_national:
                    soldire.educational_level_of_the_system = str(one_soldire_list[9])
                if has_national:
                    soldire.Study_group = str(one_soldire_list[10])
                if has_national:
                    soldire.Date_of_dispatch = str(one_soldire_list[11])
                if has_national:
                    soldire.height = str(one_soldire_list[12])
                if has_national:
                    soldire.Weight = str(one_soldire_list[13])
                if has_national:
                    soldire.province_name = str(one_soldire_list[14])
                if has_national:
                    soldire.city_name = str(one_soldire_list[15])
                if has_national:
                    soldire.Address = str(one_soldire_list[16])
                if has_national:
                    soldire.phone_number = str(one_soldire_list[17])
                if has_national:
                    soldire.home_phone_number = str(one_soldire_list[18])
                if has_national:
                    soldire.physical_condition = str(one_soldire_list[19])
                if has_national:
                    soldire.marital_status = str(one_soldire_list[20])
                soldire.willing_to_learn = False
                soldire.Sutter = "مجوز دارد"
                
                if soldire.status_type == "پیام آور بهداشت":
                    soldire.Amriye = True
                if soldire.status_type == "امریه دار":
                    soldire.Amriye = True
                if soldire.status_type == "قرارگاه سازندگی":
                    soldire.garargah_sazandegi_khatam = True
                        
                # temp = 0
                # for i in educational_level_of_the_system_list:
                #     if i[1].replace(" ", "").replace("\u200c", "") == one_soldire_list[9].replace(" ", "").replace(
                #             "\u200c", ""):
                #         temp = i[0]
                if form.cleaned_data['format_dagree']:
                    soldire.educational_level_of_the_system = smart_separation(soldire.educational_level_of_the_system) 
                    if not soldire.Study_group:
                        soldire.Study_group = soldire.educational_level_of_the_system
                        
                temp = generate_grade_temp(soldire.educational_level_of_the_system)
                soldire.Grade = categorize_educational_level(temp)[1]
                soldire.Grade_precise = map_educational_level_to_grade(temp)[1]
                soldire.date_improt_type = "سامانه"
                soldire.save()
                        

            print(f'ایجاد : {add_count} ، ویرایش : {updated_counts} ، نایده گرفته : {skipped_count}')
            messages.info(request,f'ایجاد : {add_count} ، ویرایش : {updated_counts} ، نایده گرفته : {skipped_count}')

        return render(request, 'soldiers/AddExelToDb.html', cx)

from django import forms
from django.http import HttpResponse
from openpyxl import Workbook
import pandas as pd

clabel = 'کدملی'
def excel_change_gharargah_sazandegi_khatam_true_sample(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "نمونه"
    # Header
    ws.append([clabel])
    # Sample data
    data = [["1234567890"],["0987654321" ],["2150604736"],]
    for row in data:
        ws.append(row)
    # Create response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="gharagah_sazandegi_khatam_sample.xlsx"'
    )
    # راست‌چین کردن کل شیت
    ws.sheet_view.rightToLeft = True
    wb.save(response)
    return response

from django.contrib import messages
from django.shortcuts import redirect
from .forms import FormKhatamChecked
from django import forms

def excel_change_gharargah_sazandegi_khatam_true(request):
    if request.method == 'POST':
        form = FormKhatamChecked(request.POST, request.FILES)
        if form.is_valid():
            try:
                updated_count = form.save()
                messages.success(
                    request,
                    f'{updated_count} رکورد با موفقیت به‌روز شد.'
                )
            except forms.ValidationError as e:
                messages.error(request, f'خطا در پردازش اکسل: {e}')
        else:
            messages.error(request, 'فرم نامعتبر است. لطفاً فایل و گزینه‌ها را بررسی کنید.')

    return redirect('exel')




class exel_update_number(LoginRequiredMixin, View):
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
import pandas as pd
from openpyxl.utils import get_column_letter


@login_required
def export_to_excel_list_elame_hozor(request):
    queryset = sarbaz.objects.filter(has_been_accepted=True).values(
        'acceptance_code', 'name', 'family',
        'National_Code',
        'Relative_to_inclusive_number').order_by(
        'acceptance_code')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'acceptance_code': 'کد پذیرش',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'National_Code': 'کدملی',
        'Relative_to_inclusive_number': 'شماره نسبت',
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_elame_hozor.xlsx'

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
def sater_group_print(request):
    if request.method == "GET":
        form = FormSaterGroup()
        form.fields['type'].choices = [
            (1, "عادی"),
            (2, "کفایت دار بسیج"),
            (3, "امریه دار (مامور)"),
            (4, "کفایت دار خدمت قبلی")
        ]
        return render(request, 'soldiers/sater_group_selector.html', {'form': form})

    if request.method == "POST":
        form = FormSaterGroup(request.POST, request.FILES or None)
        form.fields['type'].choices = [
            (1, "عادی"),
            (2, "کفایت دار بسیج"),
            (3, "امریه دار (مامور)"),
            (4, "کفایت دار خدمت قبلی")
        ]
        if not form.is_valid():
            return render(request, 'soldiers/sater_group_selector.html', {'form': form})

        start = int(form.cleaned_data['start'])
        end = int(form.cleaned_data['end'])+ 1
        type = int(form.cleaned_data['type'])
        en = EnsaniSettings.objects.first()

        # دیکشنری فیلترها و قالب‌ها برای هر نوع
        query_filters = {
            1: {"Amriye": False, "Sufficiency_of_mobilization": False, "in_coures": True, "has_been_accepted": True,
                "Sutter": 'مجوز دارد'},
            2: {"Sufficiency_of_mobilization": True, "has_been_accepted": True},
            3: {"Amriye": True, "Sufficiency_of_mobilization": False, "in_coures": True, "has_been_accepted": True,
                "Sutter": 'مجوز دارد'},
            4: {"Previous_service_record": True}
        }
        templates = {
            1: 'soldiers/sater_group_adi_print.html',
            2: 'soldiers/sater_group_kefayatbasij.html',
            3: 'soldiers/sater_group_amirye.html',
            4: 'soldiers/sater_group_khedmat_ghabli.html'
        }

        # دریافت سربازان بر اساس نوع و فیلترها
        if type in query_filters:
            # فیلتر کردن بر اساس acceptance_code در بازه start و end
            sarbazha = sarbaz.objects.filter(
                **query_filters[type],
                acceptance_code__gte=start,  # بزرگتر یا مساوی start
                acceptance_code__lt=end  # کوچکتر از end
            ).order_by('acceptance_code')

            for item in sarbazha:
                sr = []
                if Sater.objects.filter(sarbaz=item).first():
                    sr = Sater.objects.filter(sarbaz=item).first()
                else:
                    sr = Sater()
                sr.sarbaz = item
                sr.sater_type = type
                sr.is_get = True
                sr.sub_user = request.user
                sr.date = jdatetime.datetime.now()
                sr.save()
            return render(request, templates[type], {'sarbazha': sarbazha, 'en': en})

        # در صورت انتخاب نوع نامعتبر (بازگشت به فرم انتخاب)
        return render(request, 'soldiers/sater_group_selector.html', {'form': form})


@login_required
def moarefi_group_print(request):
    if request.method == "GET":
        form = FormMoarefiGroup()

        context = {
            'form': form,
        }
        return render(request, 'soldiers/moarefi_group_selector.html', context)
    if request.method == "POST":
        form = FormMoarefiGroup(request.POST, request.FILES or None)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'soldiers/moarefi_group_selector.html', context)
        start = int(form.cleaned_data['start'])
        end = int(form.cleaned_data['end']) + 1

        sarbazha = sarbaz.objects.filter(Sufficiency_of_mobilization=False, in_coures=True,
                                         has_been_accepted=True, willing_to_learn=True, acceptance_code__gte=start,
                                         acceptance_code__lt=end).order_by(
            'acceptance_code').all()
        en = EnsaniSettings.objects.filter().first()
        context = {
            'sarbazha': sarbazha,
            'en': en
        }
        return render(request, 'soldiers/moarefi_be_gordan_group.html', context)


@login_required
def export_soldire_has_been_accepted_in_coures_all_data(request):
    queryset = sarbaz.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'National_Code', 'name', 'family', 'fathers_name', 'acceptance_code', 'Gordan__name',
        'battalion_group__name', 'Amriye', 'Amriye_organization', 'physical_condition',
        'Type_of_disease', 'Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
        'marital_status', 'Religion', 'Date_of_birth', 'place_of_birth', 'phone_number', 'home_phone_number',
        'Date_of_dispatch', 'province_name', 'city_name', 'Address', 'Place_of_Issue', 'height', 'Weight', ).order_by(
        'acceptance_code')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'National_Code': 'کدملی',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'acceptance_code': 'عدد پذیرش',
        'Gordan__name': 'نام گردان',
        'battalion_group__name': 'نام گروهان',
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
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_has_been_accepted_in_coures.xlsx'

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
def export_soldire_has_been_accepted_all_data(request):
    queryset = sarbaz.objects.filter(has_been_accepted=True).values(
        'National_Code', 'name', 'family', 'fathers_name', 'acceptance_code', 'Gordan__name',
        'battalion_group__name', 'Amriye', 'Amriye_organization', 'physical_condition',
        'Type_of_disease', 'Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
        'marital_status', 'Religion', 'Date_of_birth', 'place_of_birth', 'phone_number', 'home_phone_number',
        'Date_of_dispatch', 'province_name', 'city_name', 'Address', 'Place_of_Issue', 'height', 'Weight', ).order_by(
        'acceptance_code')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'National_Code': 'کدملی',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'acceptance_code': 'عدد پذیرش',
        'Gordan__name': 'نام گردان',
        'battalion_group__name': 'نام گروهان',
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
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_has_been_accepted.xlsx'

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


class update_db_from_exel_paziresh_hazer_bekhdmat(LoginRequiredMixin, View):
    def get(self, request):
        form = FormUpdatePazireshHazer()
        cx = {'form': form}
        return render(request,
                      'soldiers/update_db_from_exel_paziresh_hazer_bekhdmat.html', cx)

    def post(self, request):
        form = FormUpdatePazireshHazer(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'soldiers/update_db_from_exel_paziresh_hazer_bekhdmat.html',
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
                if one_soldire_list[0] is not None:
                    find_soldire = sarbaz.objects.filter(National_Code=one_soldire_list[0]).first()
                    find_soldire.name = one_soldire_list[1]
                    find_soldire.family = one_soldire_list[2]
                    find_soldire.fathers_name = one_soldire_list[3]
                    find_soldire.acceptance_code = one_soldire_list[4]
                    gordan = battalion.objects.filter(name__icontains=str(one_soldire_list[5])).first()
                    find_soldire.Gordan = gordan
                    grohan = battalion_group.objects.filter(name__icontains=str(one_soldire_list[6]),
                                                            gordan=gordan).first()
                    find_soldire.battalion_group = grohan
                    find_soldire.Amriye = one_soldire_list[7]
                    find_soldire.Amriye_organization = one_soldire_list[8]
                    find_soldire.physical_condition = one_soldire_list[9]
                    find_soldire.Type_of_disease = one_soldire_list[10]
                    find_soldire.Grade = one_soldire_list[11]
                    find_soldire.educational_level_of_the_system = one_soldire_list[12]
                    find_soldire.Grade = one_soldire_list[13]
                    find_soldire.Study_group = one_soldire_list[14]
                    find_soldire.marital_status = one_soldire_list[15]
                    find_soldire.Religion = one_soldire_list[16]
                    find_soldire.Date_of_birth = one_soldire_list[17]
                    find_soldire.place_of_birth = one_soldire_list[18]
                    find_soldire.phone_number = one_soldire_list[19]
                    find_soldire.home_phone_number = one_soldire_list[20]
                    find_soldire.Date_of_dispatch = one_soldire_list[21]
                    find_soldire.province_name = one_soldire_list[22]
                    find_soldire.city_name = one_soldire_list[23]
                    find_soldire.Address = one_soldire_list[24]
                    find_soldire.Date_of_dispatch = one_soldire_list[25]
                    find_soldire.height = one_soldire_list[26]
                    find_soldire.Weight = one_soldire_list[27]
                    find_soldire.save()
        cx = {'form': form}
        return render(request,
                      'soldiers/update_db_from_exel_paziresh_hazer_bekhdmat.html', cx)


class update_db_from_exel_paziresh_shode(LoginRequiredMixin, View):
    def get(self, request):
        form = FormUpdatePazireshshode()
        cx = {'form': form}
        return render(request,
                      'soldiers/update_db_from_exel_paziresh_shode.html', cx)

    def post(self, request):
        form = FormUpdatePazireshshode(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'soldiers/update_db_from_exel_paziresh_shode.html',
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
                if one_soldire_list[0] is not None:
                    find_soldire = sarbaz.objects.filter(National_Code=one_soldire_list[0]).first()
                    find_soldire.name = one_soldire_list[1]
                    find_soldire.family = one_soldire_list[2]
                    find_soldire.fathers_name = one_soldire_list[3]
                    find_soldire.acceptance_code = one_soldire_list[4]
                    find_soldire.Amriye = one_soldire_list[7]
                    find_soldire.Amriye_organization = one_soldire_list[8]
                    find_soldire.physical_condition = one_soldire_list[9]
                    find_soldire.Type_of_disease = one_soldire_list[10]
                    find_soldire.Grade = one_soldire_list[11]
                    find_soldire.educational_level_of_the_system = one_soldire_list[12]
                    find_soldire.Grade = one_soldire_list[13]
                    find_soldire.Study_group = one_soldire_list[14]
                    find_soldire.marital_status = one_soldire_list[15]
                    find_soldire.Religion = one_soldire_list[16]
                    find_soldire.Date_of_birth = one_soldire_list[17]
                    find_soldire.place_of_birth = one_soldire_list[18]
                    find_soldire.phone_number = one_soldire_list[19]
                    find_soldire.home_phone_number = one_soldire_list[20]
                    find_soldire.Date_of_dispatch = one_soldire_list[21]
                    find_soldire.province_name = one_soldire_list[22]
                    find_soldire.city_name = one_soldire_list[23]
                    find_soldire.Address = one_soldire_list[24]
                    find_soldire.Date_of_dispatch = one_soldire_list[25]
                    find_soldire.height = one_soldire_list[26]
                    find_soldire.Weight = one_soldire_list[27]
                    find_soldire.save()
        cx = {'form': form}
        return render(request,
                      'soldiers/update_db_from_exel_paziresh_shode.html', cx)


@login_required
def soldier_search(request):
    query = request.GET.get('name')
    family = request.GET.get('family')
    national_code = request.GET.get('national_code')
    acceptance_code = request.GET.get('acceptance_code')
    soldiers = sarbaz.objects.all()
    if query:
        soldiers = soldiers.filter(name__icontains=query)
    if family:
        soldiers = soldiers.filter(family__icontains=family)
    if national_code:
        soldiers = soldiers.filter(National_Code__icontains=national_code)
    if acceptance_code:
        soldiers = soldiers.filter(acceptance_code=acceptance_code)

    
    context = {
        'results': soldiers,
    }
    return render(request, 'soldiers/MainViewSoldires.html', context)


@login_required
def export_to_excel_bdone_madrak_tahsili(request):
    queryset = sarbaz.objects.filter(has_been_accepted=False, Grade='نامشخص').values(
        'name', 'family', 'fathers_name',
        'National_Code', 'phone_number', 'home_phone_number')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'phone_number': 'شماره تماس',
        'home_phone_number': 'شماره تماس',

    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export_to_excel_list_bedone_madrak_samane.xlsx'

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


from django.conf import settings
import os

def get_mobilization_dir():
    en = EnsaniSettings.objects.first()  # Singleton
    dore = en.shomare_dore or 'unknown'
    return os.path.join(
        settings.MEDIA_ROOT,
        'periods',
        str(dore),
        'mobilization'
    )

def load_mobilization_files():
    base_dir = get_mobilization_dir()
    if not os.path.exists(base_dir):
        return []

    return [
        f for f in os.listdir(base_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
    ]

def get_linked_files():
    files = Soldier.objects.exclude(
        Sufficiency_of_mobilization_document=''
    ).exclude(
        Sufficiency_of_mobilization_document__isnull=True
    )

    result = {}
    for s in files:
        filename = os.path.basename(s.Sufficiency_of_mobilization_document.name)
        result[filename] = s

    return result  # {filename: soldier}

from django.shortcuts import render
import os
import zipfile
import uuid

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.conf import settings
def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 ** 2):.2f} MB"

import os
from django.conf import settings

def mobilization_document_view(request):
    all_files = load_mobilization_files()
    linked_map = get_linked_files()

    raw_files = []
    linked_files = []

    en = EnsaniSettings.objects.first()
    shomare_dore = en.shomare_dore if en and en.shomare_dore else 'unknown'

    base_dir = os.path.join(
        settings.MEDIA_ROOT,
        'periods',
        shomare_dore,
        'mobilization'
    )

    base_url = os.path.join(
        settings.MEDIA_URL,
        'periods',
        shomare_dore,
        'mobilization'
    )

    for filename in all_files:
        file_path = os.path.join(base_dir, filename)

        # اگر به هر دلیلی فایل وجود نداشت
        if not os.path.exists(file_path):
            continue

        size = format_file_size(os.path.getsize(file_path))
        url = os.path.join(base_url, filename)

        if filename in linked_map:
            linked_files.append({
                'filename': filename,
                'soldier': linked_map[filename],
                'url': url,
                'size': size,
            })
        else:
            raw_files.append({
                'filename': filename,
                'url': url,
                'size': size,
            })

    soldiers = Soldier.objects.all().order_by(
        '-Previous_service_record',
        '-Sufficiency_of_mobilization'
    )

    context = {
        'raw_files': raw_files,
        'linked_files': linked_files,
        'soldiers': soldiers,
    }

    return render(
        request,
        'functionality/mobilization_document_view.html',
        context
    )



def mobilization_document_upload(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid method')

    zip_file = request.FILES.get('zip_file')
    if not zip_file:
        return HttpResponseBadRequest('ZIP file not provided')

    # فقط zip مجاز است
    if not zip_file.name.lower().endswith('.zip'):
        return HttpResponseBadRequest('Only ZIP files are allowed')

    en = EnsaniSettings.objects.first()
    dore = en.shomare_dore if en and en.shomare_dore else 'unknown'

    # مسیر نهایی
    relative_path = os.path.join('periods', str(dore), 'mobilization')
    base_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    os.makedirs(base_path, exist_ok=True)

    allowed_ext = ('.jpg', '.jpeg', '.png', '.webp')

    with zipfile.ZipFile(zip_file) as z:
        for member in z.namelist():

            # جلوگیری از zip slip
            if '..' in member or member.startswith('/'):
                continue

            if not member.lower().endswith(allowed_ext):
                continue

            ext = os.path.splitext(member)[1]
            unique_name = f'{uuid.uuid4().hex}{ext}'
            target_path = os.path.join(base_path, unique_name)

            with z.open(member) as source, open(target_path, 'wb') as target:
                target.write(source.read())

    return redirect('mobilization_document_view')


import os
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect

@transaction.atomic
def mobilization_document_assign(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid method')

    filename = request.POST.get('filename')
    soldier_id = request.POST.get('soldier_id')

    if not filename or not soldier_id:
        return HttpResponseBadRequest('اطلاعات ناقص است')

    soldier = Soldier.objects.select_for_update().get(pk=soldier_id)
    en = EnsaniSettings.objects.first()

    dore = en.shomare_dore if en and en.shomare_dore else 'unknown'

    # مسیر فایل روی دیسک
    relative_path = os.path.join('periods',dore,'mobilization',filename)
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    if not os.path.exists(full_path):
        return HttpResponseBadRequest('فایل مورد نظر وجود ندارد')

    soldier.Sufficiency_of_mobilization_document.name = relative_path

    soldier.save(update_fields=['Sufficiency_of_mobilization_document'])

    return redirect('mobilization_document_view')


@transaction.atomic
def mobilization_document_unassign(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request')

    soldier_ids = request.POST.getlist('soldier_ids[]')

    if not soldier_ids:
        return HttpResponseBadRequest('هیچ سربازی انتخاب نشده')

    soldiers = Soldier.objects.select_for_update().filter(id__in=soldier_ids)

    for soldier in soldiers:
        soldier.Sufficiency_of_mobilization_document = None
        soldier.save(update_fields=['Sufficiency_of_mobilization_document',])

    return redirect('mobilization_document_view')

@transaction.atomic
def mobilization_document_delete(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request')

    files = request.POST.getlist('files[]')

    if not files:
        return HttpResponseBadRequest('فایلی انتخاب نشده')

    en = EnsaniSettings.objects.first()
    dore = en.shomare_dore if en else 'unknown'

    base_path = os.path.join(
        settings.MEDIA_ROOT,
        'periods',
        str(dore),
        'mobilization'
    )

    deleted = []

    for filename in files:
        # جلوگیری از path traversal
        filename = os.path.basename(filename)

        file_path = os.path.join(base_path, filename)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            deleted.append(filename)

    return redirect('mobilization_document_view')
