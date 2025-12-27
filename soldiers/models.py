from django.db import models
from skills_training.models import SlillTraining,TechnicalVocational
# Create your models here.
from battalions.models import battalion, battalion_group
from django_jalali.db import models as jmodels
from django.utils import timezone

class Soldier(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name='نام')
    family = models.CharField(null=True, blank=True, max_length=100, verbose_name='نام خانوادگی')
    fathers_name = models.CharField(null=True, blank=True, max_length=100, verbose_name='نام پدر')
    National_Code = models.CharField(null=True, blank=True, max_length=20, verbose_name='کد ملی')
    physical_condition = models.CharField(null=True, blank=True, max_length=100, verbose_name='وضعیت جسمانی')
    # تست سلامت و روان
    physical_condition_prev_test = models.CharField(null=True, blank=True, max_length=100, verbose_name='وضعیت جسمانی اولیه')
    physical_condition_test = models.CharField(null=True, blank=True, max_length=100, verbose_name='تست سلامت روان')
    physical_condition_description_test = models.CharField(null=True, blank=True, max_length=200, verbose_name='توضیحات سلامت روان')
    Type_of_disease_test = models.CharField( null=True, blank=True, max_length=250, verbose_name='نوع بیماری تست سلامت و روان')
    physical_condition_date_created = models.DateTimeField(null=True,blank=True, verbose_name='تاریخ ثبت اطلاعات')
    physical_condition_date_test = models.DateField(null=True, blank=True, verbose_name='تاریخ تست سلامت روان')
    physical_condition_Inspection_test = models.BooleanField(null=True, blank=True, verbose_name='بررسی تست سلامت روان')
    physical_condition_date_Inspection_test = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ بررسی تست سلامت روان')
    # 
    Type_of_disease = models.CharField(null=True, blank=True, max_length=250, verbose_name='نوع بیماری')
    health_insurance_card = models.CharField(null=True, blank=True, max_length=120, verbose_name='دفترچه بیمه')
    Grade = models.CharField(null=True, blank=True, max_length=200, verbose_name='مقطع تحصیلی')
    Grade_precise = models.CharField(null=True, blank=True, max_length=200, verbose_name='مقطع تحصیلی دقیق')
    educational_level_of_the_system = models.CharField(null=True, blank=True, max_length=200,verbose_name='مقطع تحصیلی سامانه')
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
    Course_renewal_date = models.CharField(null=True, blank=True, max_length=100,verbose_name='تاریخ تجدید دوره قبل')
    willing_to_learn = models.BooleanField(default=False, verbose_name='حاضر به آموزش', null=True, blank=True)
    # امریه | طرح خاتم | طرح سازندگی قرارگاه خاتم | عادی
    organization_type = models.CharField(null=True, blank=True, max_length=100,verbose_name='نوع سرباز')
    
    
    Amriye = models.BooleanField(default=False, verbose_name='امریه دار', null=True, blank=True)
    garargah_sazandegi_khatam = models.BooleanField(default=False, verbose_name='قرارگاه سازندگی خاتم', null=True, blank=True)
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
    code_gorhan = models.CharField(max_length=100, verbose_name='کدگروهان', null=True, blank=True,default="1")
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
    basij_efficiency = models.CharField(max_length=120, blank=True, null=True, verbose_name='کفایت بسیج')  # کفایت بسیج (1 نمره)
    top_three = models.CharField(max_length=100, blank=True, null=True, verbose_name='سه نفر برتر')  # سه نفر برتر (2 نمره)
    quran_memorization = models.IntegerField(default=0, verbose_name='حافظ قرآن')  # حافظ قرآن (جزء) (3 نمره)
    nahj_memorization = models.BooleanField(default=False, verbose_name='حافظ نهج البلاغه')  # حافظ نهج البلاغه (1 نمره)
    sajjadiya_memorization = models.BooleanField(default=False, verbose_name='حافظ صحیفه سجادیه')  # حافظ صحیفه سجادیه (1 نمره)
    total_score = models.FloatField(default=0, verbose_name='امتیاز کل')  # امتیاز کل
    rank = models.CharField(max_length=100, blank=True, null=True, verbose_name='درجه محاسبه‌شده')  # درجه محاسبه‌شده
    yegan_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='اسم اصلی یگان')
    tajdid_dore_moarefi_shode = models.BooleanField(default=False, verbose_name='تجدید دوره معرفی شده؟')
    
    # 🔹 مهارت اموزی
    skill_1 = models.ForeignKey(SlillTraining,null=True,blank=True,related_name="primary_soldiers",on_delete=models.SET_NULL,verbose_name="مهارت اول")
    skill_2 = models.ForeignKey(SlillTraining,null=True,blank=True,related_name="secondary_soldiers",on_delete=models.SET_NULL,verbose_name="مهارت دوم")
    # 🔹 آزمون فنی و حرفه‌ای
    technical_exam = models.ForeignKey(TechnicalVocational,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="آزمون فنی و حرفه‌ای")
    technical_exam_submit_datetime = models.DateTimeField(null=True,blank=True,verbose_name="تاریخ و زمان ثبت آزمون فنی و حرفه‌ای")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="عکس سرباز")

    # 🔹 داده‌های متفرقه (مثلاً مشکلات یا ارزیابی‌ها)
    problems_data = models.JSONField(default=dict, blank=True,verbose_name="اطلاعات مشکلات")
    
    
    def save_avatar(self, uploaded_file):
        """
        ذخیره عکس سرباز با مسیر avatars/<شماره دوره>/<کد ملی>.<ext>
        شماره دوره از EnsaniSettings گرفته می‌شود.
        """
        from ensaniapp_settings.models import EnsaniSettings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        ensani_settings = EnsaniSettings.objects.first()
        course_number = ensani_settings.shomare_dore if ensani_settings else "default"

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1]
            filename = f"{self.National_Code}.{ext}"
            file_path = f"avatars/{course_number}/{filename}"
            print(file_path)
            saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
            self.avatar = saved_path
            self.save()

    # --- توابع مدیریت تست سلامت روان ---
    def delete_test_salamat_ravan(self):
        """پاک کردن اطلاعات تست سلامت روان"""
        if self.physical_condition_Inspection_test and self.physical_condition_prev_test != self.physical_condition:
            self.physical_condition = self.physical_condition_prev_test

        self.physical_condition_prev_test = None
        self.physical_condition_test = None
        self.physical_condition_description_test = None
        self.Type_of_disease_test = None
        self.physical_condition_date_created = None
        self.physical_condition_date_test = None
        self.physical_condition_Inspection_test = None
        self.physical_condition_date_Inspection_test = None
        self.save(update_fields=[
            'physical_condition',
            'physical_condition_prev_test',
            'physical_condition_test',
            'physical_condition_description_test',
            'Type_of_disease_test',
            'physical_condition_date_created',
            'physical_condition_date_test',
            'physical_condition_Inspection_test',
            'physical_condition_date_Inspection_test'
        ])

    def confirm_test_salamat_ravan(self):
        """تایید تست سلامت روان"""
        self.physical_condition_Inspection_test = True
        self.physical_condition_date_Inspection_test = timezone.now()
        self.physical_condition = self.physical_condition_test
        self.save(update_fields=[
            'physical_condition',
            'physical_condition_Inspection_test',
            'physical_condition_date_Inspection_test'
        ])

    def unconfirm_test_salamat_ravan(self):
        """عدم تایید تست سلامت روان"""
        if self.physical_condition_Inspection_test and self.physical_condition_prev_test != self.physical_condition:
            self.physical_condition = self.physical_condition_prev_test

        self.physical_condition_Inspection_test = False
        self.physical_condition_date_Inspection_test = timezone.now()
        self.save(update_fields=[
            'physical_condition',
            'physical_condition_Inspection_test',
            'physical_condition_date_Inspection_test'
        ])
    def in_proccess_test_salamat_ravan(self):
        """درحال بررسی تست سلامت روان"""
        if self.physical_condition_Inspection_test and self.physical_condition_prev_test != self.physical_condition:
            self.physical_condition = self.physical_condition_prev_test

        self.physical_condition_Inspection_test = None
        self.physical_condition_date_Inspection_test = timezone.now()
        self.save(update_fields=[
            'physical_condition',
            'physical_condition_Inspection_test',
            'physical_condition_date_Inspection_test'
        ])

    class Meta:
        verbose_name = "سرباز"
        verbose_name_plural = "سرباز ها"


    def __str__(self):
        return f"{self.name} - {self.family} - {self.National_Code}"

