from django.db import models

# Create your models here.
from battalions.models import battalion, battalion_group
from django_jalali.db import models as jmodels


class Soldier(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name='نام')
    family = models.CharField(null=True, blank=True, max_length=100, verbose_name='نام خانوادگی')
    fathers_name = models.CharField(null=True, blank=True, max_length=100, verbose_name='نام پدر')
    National_Code = models.CharField(null=True, blank=True, max_length=20, verbose_name='کد ملی')
    physical_condition = models.CharField(null=True, blank=True, max_length=100, verbose_name='وضعیت جسمانی')
    Type_of_disease = models.CharField(null=True, blank=True, max_length=250, verbose_name='نوع بیماری')
    health_insurance_card = models.CharField(null=True, blank=True, max_length=120, verbose_name='دفترچه بیمه')
    Grade = models.CharField(null=True, blank=True, max_length=200, verbose_name='مقطع تحصیلی')
    Grade_precise = models.CharField(null=True, blank=True, max_length=200, verbose_name='مقطع تحصیلی دقیق')
    educational_level_of_the_system = models.CharField(null=True, blank=True, max_length=200,
                                                       verbose_name='مقطع تحصیلی سامانه')
    Study_group = models.CharField(null=True, blank=True, max_length=200, verbose_name='گروه تحصیلی')
    marital_status = models.CharField(null=True, blank=True, max_length=200, verbose_name='وضعیت تاهل')
    Religion = models.CharField(null=True, blank=True, max_length=50, verbose_name='مذهب')
    Date_of_birth = models.CharField(null=True, blank=True, max_length=100, verbose_name='تاریخ تولد')
    place_of_birth = models.CharField(null=True, blank=True, max_length=120, verbose_name='محل تولد')
    phone_number = models.CharField(null=True, blank=True, max_length=11, verbose_name='شماره موبایل')
    home_phone_number = models.CharField(null=True, blank=True, max_length=11, verbose_name='شماره منزل')
    Date_of_dispatch = models.CharField(null=True, blank=True, max_length=100, verbose_name='تاریخ اعزام')
    province_name = models.CharField(null=True, blank=True, max_length=150, verbose_name='نام استان')
    city_name = models.CharField(null=True, blank=True, max_length=150, verbose_name='نام شهر')
    Address = models.CharField(null=True, blank=True, max_length=250, verbose_name='ادرس')
    Place_of_Issue = models.CharField(null=True, blank=True, max_length=150, verbose_name='محل صدور')
    height = models.CharField(null=True, blank=True, max_length=10, verbose_name='قد')
    Weight = models.CharField(null=True, blank=True, max_length=10, verbose_name='وزن')

    Renewal_of_the_previous_period = models.CharField(null=True, blank=True, max_length=10,
                                                      verbose_name='تجدید دوره')
    Renewal_of_the_previous_period_code = models.CharField(null=True, blank=True, max_length=150,
                                                           verbose_name='کد تجدید دوره')
    Course_renewal_date = models.CharField(null=True, blank=True, max_length=100,
                                           verbose_name='تاریخ تجدید دوره قبل')
    willing_to_learn = models.BooleanField(default=False, verbose_name='حاضر به آموزش')
    Amriye = models.BooleanField(default=False, verbose_name='امریه دار')
    Amriye_organization = models.CharField(max_length=250, verbose_name='سازمان امریه')
    Sufficiency_of_mobilization = models.BooleanField(default=False, verbose_name='کفایت بسیج')
    the_medical_commission = models.BooleanField(default=False, verbose_name='کمیسیون پزشکی')
    has_been_accepted = models.BooleanField(default=False, verbose_name='پذیرش شده است')
    acceptance_code = models.IntegerField(null=True, blank=True, verbose_name='کد پذیرش')

    Reason_for_renewing_the_course = models.CharField(null=True, blank=True, max_length=150,
                                                      verbose_name='علت تجدید دوره')

    Previous_service_record = models.BooleanField(default=False, verbose_name='سابقه خدمت قبلی')

    attraction_of_the_organization = models.CharField(max_length=200, verbose_name='جذبی', null=True)
    Successful_recruitment = models.BooleanField(default=False, verbose_name='جذب موفق')
    Relative_to_inclusive = models.CharField(null=True, blank=True, max_length=120, verbose_name='نسبت با فراگیر')
    Relative_to_inclusive_number = models.CharField(null=True, blank=True, max_length=100,
                                                    verbose_name='شماره تماس نسبت فراگیر')
    Sutter = models.CharField(null=True, blank=True, max_length=150, verbose_name='ساتر')
    Gordan = models.ForeignKey(battalion, on_delete=models.CASCADE, verbose_name='گردان', null=True)
    battalion_group = models.ForeignKey(battalion_group, models.CASCADE, verbose_name='گروهان', null=True)

    code_paziresh = models.CharField(max_length=100, verbose_name='کدپذیرش', null=True)
    code_gorhan = models.CharField(max_length=100, verbose_name='کدگروهان', null=True)
    code_gorhan_nahai = models.CharField(max_length=100, verbose_name='کدگروهان علامی از گردان', null=True)
    tarikh_paziresh = jmodels.jDateTimeField(null=True, verbose_name='تاریخ و زمان پذیرش')


