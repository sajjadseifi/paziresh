import jdatetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from soldiers.models import Soldier
# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from .forms import CreateCheckoutLetterFrom, CreateCommissionLetterFrom, CreateRegisterLetterFrom, \
    CreateBeforeCourseCommissionLetterFrom
from .models import CheckoutLetterModels, NormalLetterModels, RegisterNormalLetter, RunawayNormallLetter

from saterapps.models import Sater
from ensaniapp_settings.models import EnsaniSettings
import random


def generate_unique_number(length=4):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


c_type_list = [(1, 'تجدید دوره'), (2, 'کمیسیون پزشکی')]

sepah_ostan_list = [
    (1, 'مازندران', 'سپاه کربلا'),
    (2, 'خراسان رضوی', 'سپاه امام رضا(ع)'),
    (3, 'خراسان شمالی', 'سپاه جوادالائمه(ع)'),
    (4, 'خراسان جنوبی', 'سپاه انصار الرضا(ع)'),
    (5, 'گلستان', 'سپاه نینوا'),
    (6, 'گیلان', 'سپاه قدس'),
    (7, 'تهران', 'سپاه حضرت محمد رسول الله (ص)'),
    (8, 'سمنان', 'سپاه قائم آل محمد(عج)'),
    (9, 'البرز', 'سپاه امام حسن مجتبی(ع)'),
    (10, 'یزد', 'سپاه الغدیر'),
    (11, 'هرمزگان', 'سپاه امام سجاد(ع)'),
    (12, 'بوشهر', 'سپاه امام صادق(ع)'),
    (13, 'ایلام', 'سپاه امیرالمومنین(ع)'),
    (14, 'همدان', 'سپاه انصار الحسین(ع)'),
    (15, 'زنجان', 'سپاه انصارالمهدی(عج)'),
    (16, 'کردستان', 'سپاه بیت المقدس'),
    (17, 'کرمان', 'سپاه ثارالله(ع)'),
    (18, 'لرستان', 'سپاه حضرت ابوالفضل(ع)'),
    (19, 'اردبیل', 'سپاه حضرت عباس(ع)'),
    (20, 'مرکزی', 'سپاه روح الله'),
    (21, 'سیستان و بلوچستان', 'سپاه سلمان'),
    (22, 'تهران', 'سپاه سیدالشهداء (ع)'),
    (23, 'آذربایجان غربی', 'سپاه شهداء'),
    (24, 'قزوین', 'سپاه صاحب الامر(عج)'),
    (25, 'اصفهان', 'سپاه صاحب الزمان(عج)'),
    (26, 'آذربایجان شرقی', 'سپاه عاشورا'),
    (27, 'قم', 'سپاه علی ابن ابیطالب(ع)'),
    (29, 'کهگیلویه و بویر احمد', 'سپاه فتح'),
    (30, 'فارس', 'سپاه فجر'),
    (31, 'چهارمحال و بختیاری', 'سپاه قمر بنی هاشم(ع)'),
    (32, 'کرمانشاه', 'سپاه نبی اکرم(ص)'),
    (33, 'خوزستان', 'سپاه ولیعصر(عج)'),
]
sepah_ostan_list2 = []
for item in sepah_ostan_list:
    sepah_ostan_list2.append((item[0], F"{item[1]}-{item[2]}"))


def find_sepah(p):
    for item in sepah_ostan_list:
        if item[1] == p:
            return item[0]
    return 0


def find_sepah_name(p):
    for iteam in sepah_ostan_list:
        if iteam[1] == str(p):
            return iteam[2]


def AllCheckoutLetter(request, *args, **kwargs):
    all_checkout_letter = CheckoutLetterModels.objects.filter().all()
    return render(request, 'ensani_letter/all_checkout_letter.html',
                  context={'all_checkout_letter': all_checkout_letter})


class CreateCheckoutLetter(LoginRequiredMixin, View):
    template = 'ensani_letter/create_checkout_letter.html'
    success_url = reverse_lazy('AllCheckoutLetter')

    def get(self, request):
        soldire_list = []
        g = Soldier.objects.filter(IsCheckout=False).all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateCheckoutLetterFrom()
        b_form.fields['soldire'].choices = soldire_list
        b_form.fields['c_type'].choices = c_type_list
        cx = {'form': b_form}
        return render(request, self.template, cx)

    def post(self, request):
        soldire_list = []
        g = Soldier.objects.filter().all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateCheckoutLetterFrom(request.POST, request.FILES or None)
        b_form.fields['soldire'].choices = soldire_list
        b_form.fields['c_type'].choices = c_type_list
        if not b_form.is_valid():
            cx = {'form': b_form}
            return render(request, self.template, cx)
        my_letter = CheckoutLetterModels()
        my_letter.description = b_form.cleaned_data['description']
        find_soldire = Soldier.objects.filter(National_Code=b_form.cleaned_data['soldire']).first()
        find_soldire.IsCheckout = True
        find_soldire.willing_to_learn = False
        find_soldire.save()
        my_letter.soldire = find_soldire
        my_letter.status = "ثبت اولیه"
        my_letter.create_time = jdatetime.datetime.now()
        ens = EnsaniSettings.objects.filter().first()
        my_letter.number = F"{ens.shomare_dore}{generate_unique_number()}{find_soldire.National_Code[::3]}"
        c_type = ""
        for iteam in c_type_list:
            if iteam[0] == int(b_form.cleaned_data['c_type']):
                c_type = iteam[1]
        my_letter.c_type = c_type
        my_letter.save()
        return redirect(self.success_url)


def AllNormalLetter(request, *args, **kwargs):
    all_normal_letter = NormalLetterModels.objects.filter().all()
    return render(request, 'ensani_letter/all_normal_letter.html',
                  context={'all_normal_letter': all_normal_letter})


class CreateCommissionLetter(LoginRequiredMixin, View):
    template = 'ensani_letter/create_commission_letter.html'
    success_url = reverse_lazy('AllNormalLetter')

    def get(self, request, pk):
        b_form = CreateCommissionLetterFrom()
        b_form.fields['destination'].choices = sepah_ostan_list2
        b_form.initial['subject'] = "معرفی به کمیسیون"
        cl = CheckoutLetterModels.objects.filter(number=pk).first()
        b_form.initial['destination'] = find_sepah(cl.soldire.province_name)
        cx = {'form': b_form, 'cl': cl}
        return render(request, self.template, cx)

    def post(self, request, pk):
        b_form = CreateCommissionLetterFrom(request.POST, request.FILES or None)
        b_form.fields['destination'].choices = sepah_ostan_list2
        b_form.initial['subject'] = "معرفی به کمیسیون"
        cl = CheckoutLetterModels.objects.filter(number=pk).first()
        b_form.initial['destination'] = find_sepah(cl.soldire.province_name)
        if not b_form.is_valid():
            cx = {'form': b_form, 'cl': cl}
            return render(request, self.template, cx)
        my_letter = NormalLetterModels()
        my_letter.description = b_form.cleaned_data['description']
        my_letter.subject = b_form.cleaned_data['subject']
        find_soldire = Soldier.objects.filter(id=cl.soldire.id).first()
        my_letter.soldire = find_soldire
        find_soldire.the_medical_commission = True
        cl.status = "درحال معرفی به کمیسیون"
        my_letter.create_time = jdatetime.datetime.now()
        ens = EnsaniSettings.objects.filter().first()
        my_letter.number = F"{ens.shomare_dore}00{generate_unique_number()}{find_soldire.National_Code[::3]}"
        destination = ""
        for iteam in sepah_ostan_list:
            if iteam[0] == int(b_form.cleaned_data['destination']):
                destination = iteam[2]
        my_letter.destination = destination
        my_letter.save()
        find_soldire.save()
        return redirect(self.success_url)


class CreateBeforeCourseCommissionLetter(LoginRequiredMixin, View):
    template = 'ensani_letter/create_before_course_commission_letter.html'
    success_url = reverse_lazy('AllNormalLetter')

    def get(self, request):
        soldire_list = []
        g = Soldier.objects.filter().all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateBeforeCourseCommissionLetterFrom()
        b_form.fields['soldire'].choices = soldire_list
        cx = {'form': b_form}
        return render(request, self.template, cx)

    def post(self, request):
        soldire_list = []
        g = Soldier.objects.filter().all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateBeforeCourseCommissionLetterFrom(request.POST, request.FILES or None)
        b_form.fields['soldire'].choices = soldire_list
        if not b_form.is_valid():
            cx = {'form': b_form}
            return render(request, self.template, cx)
        my_letter = NormalLetterModels()
        my_letter.description = b_form.cleaned_data['description']
        my_letter.subject = "معرفی به کمیسیون شروع دوره آموزشی"
        soldire_code_meli = b_form.cleaned_data['soldire']
        find_soldire = Soldier.objects.filter(National_Code=soldire_code_meli).first()
        my_letter.soldire = find_soldire
        my_letter.create_time = jdatetime.datetime.now()
        ens = EnsaniSettings.objects.filter().first()
        my_letter.number = F"{ens.shomare_dore}33{generate_unique_number()}{find_soldire.National_Code[::3]}"
        destination = find_sepah_name(find_soldire.province_name)
        my_letter.destination = destination
        my_letter.status = "تایید"
        my_letter.save()
        all_find_solidre = Soldier.objects.filter(has_been_accepted=True).all().count()
        if find_soldire.willing_to_learn is True:
            find_soldire.willing_to_learn = False
        find_soldire.the_medical_commission = True
        if find_soldire.acceptance_code is not None:
            find_soldire.acceptance_code = all_find_solidre + 1
        find_soldire.in_coures = False
        find_soldire.has_been_accepted = True
        find_soldire.save()
        return redirect(self.success_url)


class CreateTrainingInquiryLetter(LoginRequiredMixin, View):
    template = 'ensani_letter/create_training_inquiry_letter.html'
    success_url = reverse_lazy('AllNormalLetter')
    soldire_list = []
    g = Soldier.objects.filter().all()
    for item in g:
        soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))

    def get(self, request):
        soldire_list = []
        g = Soldier.objects.filter().all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateCheckoutLetterFrom()
        b_form.fields['soldire'].choices = soldire_list
        cx = {'form': b_form}
        return render(request, self.template, cx)

    def post(self, request):
        soldire_list = []
        g = Soldier.objects.filter().all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateCheckoutLetterFrom(request.POST, request.FILES or None)
        b_form.fields['soldire'].choices = soldire_list
        if not b_form.is_valid():
            cx = {'form': b_form}
            return render(request, self.template, cx)
        my_letter = NormalLetterModels()
        all_find_solidre = Soldier.objects.filter(has_been_accepted=True).all().count()
        find_soldire = Soldier.objects.filter(National_Code=b_form.cleaned_data['soldire']).first()
        find_soldire.has_been_accepted = True
        find_soldire.acceptance_code = all_find_solidre + 1
        find_soldire.willing_to_learn = False
        find_soldire.code_paziresh = all_find_solidre + 1
        find_soldire.Previous_service_record = True
        find_soldire.save()
        my_letter.soldire = find_soldire
        my_letter.status = "درحال بررسی"
        my_letter.create_time = jdatetime.datetime.now()
        my_letter.description = "استعلام کفایت از آموزش"
        my_letter.destination = "آموزش"
        my_letter.subject = "استعلام کفایت از آموزش"
        ens = EnsaniSettings.objects.filter().first()
        my_letter.number = my_letter.number = F"{ens.shomare_dore}99{generate_unique_number()}{find_soldire.National_Code[::3]}"
        my_letter.save()
        return redirect(self.success_url)


class CreateRegisterLetter(LoginRequiredMixin, View):
    template = 'ensani_letter/create_register_letter.html'
    success_url = reverse_lazy('AllNormalLetter')
    soldire_list = []
    g = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).all()
    for item in g:
        soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))

    def get(self, request):
        soldire_list = []
        g = Soldier.objects.filter().all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateRegisterLetterFrom()
        b_form.fields['soldire'].choices = soldire_list
        cx = {'form': b_form}
        return render(request, self.template, cx)

    def post(self, request):
        soldire_list = []
        g = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateRegisterLetterFrom(request.POST, request.FILES or None)
        b_form.fields['soldire'].choices = soldire_list
        if not b_form.is_valid():
            cx = {'form': b_form}
            return render(request, self.template, cx)
        my_letter = NormalLetterModels()
        find_soldire = Soldier.objects.filter(National_Code=b_form.cleaned_data['soldire']).first()
        my_letter.soldire = find_soldire
        my_letter.create_time = jdatetime.datetime.now()
        my_letter.description = "گواهی عضویت"
        my_letter.destination = b_form.cleaned_data['destination']
        my_letter.subject = "گواهی عضویت"
        ens = EnsaniSettings.objects.filter().first()
        my_letter.number = my_letter.number = F"{ens.shomare_dore}99{generate_unique_number()}{find_soldire.National_Code[::3]}"
        my_letter.status = "تایید"
        my_letter.save()
        rn = RegisterNormalLetter()
        rn.normal_letter = my_letter
        in_come_letter_numbers = b_form.cleaned_data['destination_letter_number']
        in_come_letter_date = b_form.cleaned_data['destination_letter_date']
        in_come_submit_locations = b_form.cleaned_data['in_come_submit_locations']
        if in_come_submit_locations is not None:
            rn.in_come_submit_locations = in_come_submit_locations
        if in_come_letter_date is not None:
            rn.in_come_letter_data = in_come_letter_date
        if in_come_letter_numbers is not None:
            rn.in_come_letter_numbers = in_come_letter_numbers
        rn.save()
        return redirect(self.success_url)


class CreaterunawayLetter(LoginRequiredMixin, View):
    template = 'ensani_letter/create_runaway_letter.html'
    success_url = reverse_lazy('AllNormalLetter')
    soldire_list = []
    g = Soldier.objects.filter(IsCheckout=True).all()
    for item in g:
        soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))

    def get(self, request):
        soldire_list = []
        g = Soldier.objects.filter().all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateRegisterLetterFrom()
        b_form.fields['soldire'].choices = soldire_list
        cx = {'form': b_form}
        return render(request, self.template, cx)

    def post(self, request):
        soldire_list = []
        g = Soldier.objects.filter(IsCheckout=True).all()
        for item in g:
            soldire_list.append((item.National_Code, F"{item.name} {item.family}  - {item.National_Code}"))
        b_form = CreateRegisterLetterFrom(request.POST, request.FILES or None)
        b_form.fields['soldire'].choices = soldire_list
        if not b_form.is_valid():
            cx = {'form': b_form}
            return render(request, self.template, cx)
        my_letter = NormalLetterModels()
        find_soldire = Soldier.objects.filter(National_Code=b_form.cleaned_data['soldire']).first()
        my_letter.soldire = find_soldire
        my_letter.create_time = jdatetime.datetime.now()
        my_letter.description = "فرار"
        my_letter.destination = b_form.cleaned_data['destination']
        my_letter.subject = "فرار"
        ens = EnsaniSettings.objects.filter().first()
        my_letter.number = my_letter.number = F"{ens.shomare_dore}99{generate_unique_number()}{find_soldire.National_Code[::3]}"
        my_letter.status = "تایید"
        my_letter.save()
        rn = RegisterNormalLetter()
        rn.normal_letter = my_letter
        in_come_letter_numbers = b_form.cleaned_data['destination_letter_number']
        in_come_letter_date = b_form.cleaned_data['destination_letter_date']
        in_come_submit_locations = b_form.cleaned_data['in_come_submit_locations']
        if in_come_submit_locations is not None:
            rn.in_come_submit_locations = in_come_submit_locations
        if in_come_letter_date is not None:
            rn.in_come_letter_data = in_come_letter_date
        if in_come_letter_numbers is not None:
            rn.in_come_letter_numbers = in_come_letter_numbers
        rn.save()
        return redirect(self.success_url)


def PrintCheckoutLetter(request, *args, **kwargs):
    checkout_letter_pk = kwargs['pk']
    if checkout_letter_pk is None:
        return 0
    checkout_letter = CheckoutLetterModels.objects.filter(pk=checkout_letter_pk).first()
    checkout_letter.status = "چاپ برگه-درحال بررسی"
    checkout_letter.save()
    en = EnsaniSettings.objects.filter().first()
    cx = {'checkout_letter': checkout_letter, 'en': en}
    return render(request, 'ensani_letter/print_checkout_letter.html', cx)


def PrintCheckoutCommissionLetter(request, *args, **kwargs):
    checkout_commission_letter_pk = kwargs['pk']
    if checkout_commission_letter_pk is None:
        return 0
    en = EnsaniSettings.objects.filter().first()
    checkout_commission_letter = NormalLetterModels.objects.filter(pk=checkout_commission_letter_pk).first()
    sutter = Sater.objects.filter(sarbaz=checkout_commission_letter.soldire).first()
    checkout_commission_letter.status = "تجدید دوره کمیسیون"
    cx = {'checkout_commission_letter': checkout_commission_letter, 'sutter': sutter, 'en': en}
    return render(request, 'ensani_letter/print_checkout_commission_letter.html', cx)


def PrintTrainingInquiryLetter(request, *args, **kwargs):
    training_inquiry_letter_pk = kwargs['pk']
    if training_inquiry_letter_pk is None:
        return 0
    training_inquiry_letter = NormalLetterModels.objects.filter(pk=training_inquiry_letter_pk).first()
    en = EnsaniSettings.objects.filter().first()
    cx = {'training_inquiry_letter': training_inquiry_letter, 'en': en}
    return render(request, 'ensani_letter/print_training_inquiry_letter.html', cx)


def PrintRegisterLetter(request, *args, **kwargs):
    Normal_letter = kwargs['pk']
    if Normal_letter is None:
        return 0
    Normal_letter_Register = NormalLetterModels.objects.filter(pk=Normal_letter).first()
    Rg = RegisterNormalLetter.objects.filter(normal_letter=Normal_letter_Register).first()
    en = EnsaniSettings.objects.filter().last()
    cx = {'Normal_letter_Register': Normal_letter_Register, 'en': en, 'rg': Rg}
    return render(request, 'ensani_letter/print_register_normal_letter.html', cx)


def PrintBeforeCourseCommissionLetter(request, *args, **kwargs):
    before_course_commission_letter_pk = kwargs['pk']
    if before_course_commission_letter_pk is None:
        return 0
    before_course_commission = NormalLetterModels.objects.filter(pk=before_course_commission_letter_pk).first()
    cx = {'before_course_commission_letter': before_course_commission}
    return render(request, 'ensani_letter/print_before_course_commission_letter.html', cx)


def PrintRunawayLetterLetter(request, *args, **kwargs):
    Runaway_letter_pk = kwargs['pk']
    if Runaway_letter_pk is None:
        return 0
    Runaway = NormalLetterModels.objects.filter(pk=Runaway_letter_pk).first()
    en = EnsaniSettings.objects.filter().last()
    cx = {' Runaway': Runaway, 'en': en}
    return render(request, 'ensani_letter/print_runaway_letter_letter.html', cx)


def check_status_checkout(request, *args, **kwargs):
    checkout_id = kwargs['pk']
    if checkout_id is None:
        return redirect(reverse_lazy('AllCheckoutLetter'))
    checkout_letter = CheckoutLetterModels.objects.filter(pk=checkout_id).first()
    checkout_letter.status = "تایید"
    checkout_letter.save()
    return redirect(reverse_lazy('AllCheckoutLetter'))


def remove_checkout(request, *args, **kwargs):
    checkout_id = kwargs['pk']
    if checkout_id is None:
        return redirect(reverse_lazy('AllCheckoutLetter'))
    checkout_letter = CheckoutLetterModels.objects.filter(pk=checkout_id).first()
    checkout_letter.soldire.IsCheckout = False
    checkout_letter.soldire.in_coures = True
    checkout_letter.soldire.willing_to_learn = True
    if checkout_letter.soldire.the_medical_commission == True:
        n = NormalLetterModels.objects.filter(subject='معرفی به کمیسیون', soldire=checkout_letter.soldire).all()
        if n is not None:
            n.delete()
            checkout_letter.soldire.the_medical_commission = False
    checkout_letter.delete()
