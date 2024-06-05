from django.db import models
from soldiers.models import Soldier
from django_jalali.db import models as jmodels


# Create your models here.


class NormalLetterModels(models.Model):
    subject = models.CharField(max_length=100, verbose_name='موضوع نامه')
    soldire = models.ForeignKey(Soldier, on_delete=models.CASCADE, verbose_name='سرباز')
    create_time = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ')
    destination = models.CharField(max_length=150, verbose_name='مقصد نامه', null=True, blank=True)
    description = models.CharField(max_length=150, verbose_name='توضیحات', null=True, blank=True)


class CheckoutLetterModels(models.Model):
    create_time = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ')
    soldire = models.ForeignKey(Soldier, on_delete=models.CASCADE, verbose_name='سرباز')
    destination = models.CharField(max_length=150, verbose_name='مقصد نامه', null=True, blank=True)
    description = models.CharField(max_length=150, verbose_name='توضیحات', null=True, blank=True)
