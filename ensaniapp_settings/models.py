from django.db import models
from django_jalali.db import models as jmodels
import os
import uuid
from django.conf import settings

class EnsaniSettings(models.Model):
    # DORE
    shomare_dore = models.CharField(null=True, blank=True, max_length=100, verbose_name='شماره دوره')
    esmedore = models.CharField(null=True, blank=True, max_length=250, verbose_name='نام دوره')
    tarikhezam = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ اعزام')
    tatbigh = models.BooleanField(default=False, verbose_name='آمار پس از تطبیق')
    mahezam = models.CharField(max_length=100, verbose_name='ماه اعزارم', null=True, blank=True)
    sall = models.CharField(max_length=100, verbose_name='سال', null=True, blank=True)

    # PAZIRESH
    tarikhpaziresh = jmodels.jDateField(null=True, verbose_name='تاریخ شروع پذیرش')
    tarikhetmampaziresh = jmodels.jDateField(null=True, verbose_name='تاریخ پایان پذیرش')
    tarihkeshorodoreh = jmodels.jDateField(null=True, verbose_name='تاریخ شروع دوره')
    tarihkepayanedore = jmodels.jDateField(null=True, verbose_name='تاریخ پایان دوره')
    saghf_paziresh = models.CharField(null=True, blank=True, max_length=100, verbose_name='سقف پذیرش')

    # LETTERS
    shoare_sall = models.CharField(null=True, blank=True, max_length=100, verbose_name='شعار سال')
    saghfi_eblaghi = models.CharField(max_length=100, verbose_name='سقف نامه', null=True, blank=True)
    shomare_name_shoro_doreh = models.CharField(max_length=100, verbose_name='شماره نامه ابلاغ دوره', null=True,blank=True)
    tarihke_name_shoro_doreh = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ نامه ابلاغ دوره')
    
    farmande_razme_moghadamati = models.CharField(null=True, blank=True, max_length=100,verbose_name='فرمانده آموزشگاه')
    modire_niroye_ensani = models.CharField(null=True, blank=True, max_length=100,verbose_name='مدیر نیروی انسانی')
    karshenas_manabe_ensani = models.CharField(null=True, blank=True, max_length=100,verbose_name='کارشناس منابع انسانی سرباز')
    
    # GARDESHKAR 
    hokme_darje_shomare_name = models.CharField(max_length=100, verbose_name='سقف نامه', null=True, blank=True,default='')
    hokme_darje_gardeshkar = models.CharField(max_length=100, null=True, blank=True,verbose_name='شماره گردشکار حکم درجه')
    tarikh_hokme_darje_gardeshkar = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ گردش کار حکم درجه')

    # SIGNUTURE
    emza_karshenas_manabe_ensani = models.ImageField(upload_to='images/', null=True, blank=True,verbose_name='امضای کارشناس منابع سرباز')
    emza_masole_niro_ensani = models.ImageField(upload_to='images/', null=True, blank=True,verbose_name='امضای مدیر نیروانسانی')
    emza_farmande = models.ImageField(upload_to='images/', null=True, blank=True,verbose_name='امضای فرمانده آموزشگاه')

    class Meta:
        verbose_name = "تنظیمات"
        verbose_name_plural = "تنظیمات"
        

def period_upload_path(subdir: str):
    def _path(instance, filename):
        en = EnsaniSettings.objects.first()  # Singleton

        relative_path = f'periods/{en.shomare_dore}/{subdir}'
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        # ساخت پوشه اگر وجود نداشت
        os.makedirs(full_path, exist_ok=True)

        return f'{relative_path}/{filename}'

    return _path


import os
import uuid
from django.conf import settings

def mobilization_upload_path(instance, filename):
    """
    مسیر ذخیره فایل سند کفایت بسیج:

    media/periods/{shomare_dore}/mobilization/{unique_filename}
    """

    # فقط هنگام save اجرا می‌شود، پس هیچ warning در import نمی‌دهد
    en = getattr(instance, 'ensani_settings', None)
    if en is None:
        # fallback اگر instance فاقد ensani_settings باشد
        dore = 'unknown'
    else:
        # اگر shomare_dore تهی باشد، unknown استفاده می‌شود
        dore = getattr(en, 'shomare_dore', 'unknown') or 'unknown'

    # مسیر نسبی
    relative_path = os.path.join('periods', str(dore), 'mobilization')

    # مسیر کامل روی دیسک
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    os.makedirs(full_path, exist_ok=True)  # ایجاد پوشه اگر وجود نداشت

    # یونیک کردن نام فایل با uuid
    ext = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{ext}"

    return os.path.join(relative_path, unique_filename)
