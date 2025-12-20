from django.db import models
from django_jalali.db import models as jmodels

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