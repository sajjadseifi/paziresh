from django.db import models
from django_jalali.db import models as jmodels


# Create your models here.


class EnsaniSettings(models.Model):
    farmande_razme_moghadamati = models.CharField(null=True, blank=True, max_length=100,
                                                  verbose_name='فرمانده آموزشگاه رزم مقدماتی')
    modire_niroye_ensani = models.CharField(null=True, blank=True, max_length=100,
                                            verbose_name='مدیر نیروی انسانی آموزشگاه رزم مقدماتی')
    karshenas_manabe_ensani = models.CharField(null=True, blank=True, max_length=100,
                                               verbose_name='کارشناس منابع انسانی سرباز آموزشگاه رزم مقدماتی')
    shoare_sall = models.CharField(null=True, blank=True, max_length=100, verbose_name='شعار سال')
    shomare_dore = models.CharField(null=True, blank=True, max_length=100, verbose_name='شماره دوره')
    esmedore = models.CharField(null=True, blank=True, max_length=250, verbose_name='نام دوره')
    tarikhpaziresh = jmodels.jDateField(null=True, verbose_name='تاریخ شروع پذیرش')
    tarikhetmampaziresh = jmodels.jDateField(null=True, verbose_name='تاریخ پایان پذیرش')
    tarihkeshorodoreh = jmodels.jDateField(null=True, verbose_name='تاریخ شروع دوره')
    tarihkepayanedore = jmodels.jDateField(null=True, verbose_name='تاریخ پایان دوره')
    saghf_paziresh = models.CharField(null=True, blank=True, max_length=100, verbose_name='سقف پذیرش')
    tarikhezam = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ اعزام')
    tatbigh = models.BooleanField(default=False, verbose_name='آمار پس از تطبیق')
