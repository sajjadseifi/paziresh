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

    Renewal_of_the_previous_period = models.CharField(null=True, blank=True, max_length=100,
                                                      verbose_name='تجدید دوره')
    Renewal_of_the_previous_period_code = models.CharField(null=True, blank=True, max_length=150,
                                                           verbose_name='کد تجدید دوره')
    Course_renewal_date = models.CharField(null=True, blank=True, max_length=100,
                                           verbose_name='تاریخ تجدید دوره قبل')
    willing_to_learn = models.BooleanField(default=False, verbose_name='حاضر به آموزش', null=True, blank=True)
    Amriye = models.BooleanField(default=False, verbose_name='امریه دار', null=True, blank=True)
    Amriye_organization = models.CharField(max_length=250, verbose_name='سازمان امریه', null=True, blank=True)
    Sufficiency_of_mobilization = models.BooleanField(default=False, verbose_name='کفایت بسیج', blank=True, null=True)
    the_medical_commission = models.BooleanField(default=False, verbose_name='کمیسیون پزشکی', blank=True, null=True)
    has_been_accepted = models.BooleanField(default=False, verbose_name='پذیرش شده است', blank=True, null=True)
    acceptance_code = models.IntegerField(null=True, blank=True, verbose_name='کد پذیرش', unique=True)

    Reason_for_renewing_the_course = models.CharField(null=True, blank=True, max_length=150,
                                                      verbose_name='علت تجدید دوره')

    Previous_service_record = models.BooleanField(default=False, verbose_name='سابقه خدمت قبلی', blank=True, null=True)

    attraction_of_the_organization = models.CharField(max_length=200, default='هیچکدام',
                                                      verbose_name='جذبی', null=True, blank=True)
    Successful_recruitment = models.BooleanField(default=False, verbose_name='جذب موفق', blank=True, null=True)
    Relative_to_inclusive = models.CharField(null=True, blank=True, max_length=120, verbose_name='نسبت با فراگیر')
    Relative_to_inclusive_number = models.CharField(null=True, blank=True, max_length=100,
                                                    verbose_name='شماره تماس نسبت فراگیر')
    Sutter = models.CharField(null=True, blank=True, max_length=150, verbose_name='ساتر')
    Gordan = models.ForeignKey('battalions.battalion', on_delete=models.CASCADE, verbose_name='گردان', null=True,
                               blank=True)
    battalion_group = models.ForeignKey('battalions.battalion_group', models.CASCADE, verbose_name='گروهان', null=True,
                                        blank=True)
    t_Gordan = models.ForeignKey('battalions.battalion', on_delete=models.CASCADE, verbose_name='گردان', null=True,
                                 blank=True,
                                 related_name='gordan_after_tatbigh')
    t_battalion_group = models.ForeignKey('battalions.battalion_group', models.CASCADE, verbose_name='گروهان',
                                          null=True, blank=True,
                                          related_name='gorohan_after_tatbigh')
    code_paziresh = models.CharField(max_length=100, verbose_name='کدپذیرش', null=True, blank=True)
    code_gorhan = models.CharField(max_length=100, verbose_name='کدگروهان', null=True, blank=True)
    code_gorhan_nahai = models.IntegerField(verbose_name='کدگروهان علامی از گردان', null=True, blank=True)
    tarikh_paziresh = jmodels.jDateTimeField(null=True, verbose_name='تاریخ و زمان پذیرش', blank=True)
    IsCheckout = models.BooleanField(default=False, verbose_name='تسویه حساب', blank=True, null=True)
    unit_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='نام یگان')
    unit_type = models.CharField(max_length=200, blank=True, null=True, verbose_name='نوع یگان')
    unit_address = models.CharField(max_length=200, blank=True, null=True, verbose_name='ادرس یگان')
    unit_province = models.CharField(max_length=200, blank=True, null=True, verbose_name='استان یگیان')
    date_improt_type = models.CharField(max_length=200, verbose_name='اطلاعات', null=True, blank=True)
    in_coures = models.BooleanField(default=False, verbose_name='شرکت در دوره')
    tatbigh = models.BooleanField(default=False, verbose_name='تطبیق شده/نشده')
    IsUnit = models.BooleanField(default=False, verbose_name='وضعیت یگان')
    bank_number = models.CharField(max_length=250, verbose_name='شماره حساب', null=True, blank=True)

    # فیلدهای مرتبط با امتیازات مختلف
    discipline_score = models.FloatField(default=0, verbose_name='انضباط')  # انضباط (2 نمره)
    basij_experience = models.FloatField(default=0,
                                         verbose_name='سابقه بسیج فعال به ماه')  # سابقه بسیج فعال به ماه (2 نمره)
    council_experience = models.FloatField(default=0,
                                           verbose_name='سابقه عضو شورای پایگاه به ماه')  # سابقه عضو شورای پایگاه به ماه (1 نمره)
    ideological_score = models.FloatField(default=0, verbose_name='نمره عقیدتی')  # نمره عقیدتی (1 نمره)
    shooting_score = models.FloatField(default=0, verbose_name='نمره میدان تیر')  # نمره میدان تیر (2 نمره)
    global_awards = models.IntegerField(default=0, verbose_name='تعداد مقام جهانی')  # تعداد مقام جهانی
    national_awards = models.IntegerField(default=0, verbose_name='تعداد مقام کشوری')  # تعداد مقام کشوری
    provincial_awards = models.IntegerField(default=0, verbose_name='تعداد مقام استانی')  # تعداد مقام استانی
    global_articles = models.IntegerField(default=0, verbose_name='تعداد مقالات جهانی')  # تعداد مقالات جهانی
    publications = models.IntegerField(default=0, verbose_name='تعداد تالیفات')  # تعداد تالیفات
    repeat_status = models.BooleanField(default=False, verbose_name='تکراری')  # تکراری
    battalion_activity = models.FloatField(default=0, verbose_name='فعالیت در گردان')  # فعالیت در گردان (2.5 نمره)
    battalion_sample = models.BooleanField(default=False, verbose_name='نمونه گردان')  # نمونه گردان (2 نمره مازاد)
    basij_efficiency = models.CharField(max_length=120, blank=True, null=True,
                                        verbose_name='کفایت بسیج')  # کفایت بسیج (1 نمره)
    top_three = models.CharField(max_length=100, blank=True, null=True,
                                 verbose_name='سه نفر برتر')  # سه نفر برتر (2 نمره)
    quran_memorization = models.IntegerField(default=0, verbose_name='حافظ قرآن')  # حافظ قرآن (جزء) (3 نمره)
    nahj_memorization = models.BooleanField(default=False, verbose_name='حافظ نهج البلاغه')  # حافظ نهج البلاغه (1 نمره)
    sajjadiya_memorization = models.BooleanField(default=False,
                                                 verbose_name='حافظ صحیفه سجادیه')  # حافظ صحیفه سجادیه (1 نمره)
    total_score = models.FloatField(default=0, verbose_name='امتیاز کل')  # امتیاز کل
    rank = models.CharField(max_length=100, blank=True, null=True, verbose_name='درجه محاسبه‌شده')  # درجه محاسبه‌شده
    yegan_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='اسم اصلی یگان')
    tajdid_dore_moarefi_shode = models.BooleanField(default=False, verbose_name='تجدید دوره معرفی شده؟')

    class Meta:
        verbose_name = "سرباز"
        verbose_name_plural = "سرباز ها"


    def __str__(self):
        return f"{self.name} - {self.family} - {self.National_Code}"
