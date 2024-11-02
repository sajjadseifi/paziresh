from django.db import models
from soldiers.models import Soldier
from django_jalali.db import models as jmodels


class NormalLetterModels(models.Model):
    subject = models.CharField(max_length=100, verbose_name='موضوع نامه')
    soldire = models.ForeignKey(Soldier, on_delete=models.CASCADE, verbose_name='سرباز')
    create_time = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ')
    destination = models.CharField(max_length=150, verbose_name='مقصد نامه', null=True, blank=True)
    description = models.CharField(max_length=150, verbose_name='توضیحات', null=True, blank=True)
    number = models.CharField(max_length=200, verbose_name='شماره نامه', null=True, blank=True)
    status = models.CharField(max_length=200, verbose_name='وضعیت', null=True, blank=True)

    def __str__(self):
        return self.soldire.name + " " + self.soldire.family


class CheckoutLetterModels(models.Model):
    create_time = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ')
    soldire = models.ForeignKey(Soldier, on_delete=models.CASCADE, verbose_name='سرباز')
    description = models.CharField(max_length=150, verbose_name='توضیحات', null=True, blank=True)
    number = models.CharField(max_length=250, verbose_name='شماره نامه')
    c_type = models.CharField(max_length=250, verbose_name='علت تسویه حساب')
    status = models.CharField(max_length=200, verbose_name='وضعیت', null=True, blank=True)

    def __str__(self):
        return self.soldire.name + " " + self.soldire.family

    def find_com(self):
        n = NormalLetterModels.objects.filter(subject='معرفی به کمیسیون', soldire=self.soldire).all()
        return n


class RegisterNormalLetter(models.Model):
    in_come_letter_numbers = models.CharField(max_length=100, verbose_name='شماره نامه وارده', null=True, blank=True)
    in_come_letter_data = models.CharField(max_length=100, verbose_name='تاریخ نامه وارده', null=True, blank=True)
    in_come_submit_locations = models.CharField(max_length=100, verbose_name='مبدا صادر کننده', null=True, blank=True)
    normal_letter = models.ForeignKey(NormalLetterModels, on_delete=models.CASCADE, verbose_name='نامه عادی')


class RunawayNormallLetter(models.Model):
    type = models.CharField(max_length=120, verbose_name='دلیل فرار', null=True, blank=True)
    run_away_dated = models.CharField(max_length=120, verbose_name='تاریخ فرار', null=True, blank=True)
    normal_letter = models.ForeignKey(NormalLetterModels, on_delete=models.CASCADE, verbose_name='نامه عادی')
