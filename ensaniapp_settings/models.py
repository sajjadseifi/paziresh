from django.db import models


# Create your models here.


class EnsaniSettings(models.Model):
    esmedore = models.CharField(null=True, blank=True, max_length=250, verbose_name='نام دوره')
    tarikhpaziresh = models.CharField(null=True, blank=True, max_length=100, verbose_name='تاریخ پذیرش')
    tarikhetmampaziresh = models.CharField(null=True, blank=True, max_length=100, verbose_name='تاریخ اتمام پذیرش')
    tarihkeshorodoreh = models.CharField(null=True, blank=True, max_length=100, verbose_name='تاریخ شروع دوره')
    tarihkepayanedore = models.CharField(null=True, blank=True, max_length=100, verbose_name='تاریخ اتمام دوره')
    modiremanabeensani = models.CharField(null=True, blank=True, max_length=100, verbose_name='نام مدیر نیروی انسانی')
