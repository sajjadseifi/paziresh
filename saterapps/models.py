from django.contrib.auth.models import User
from django.db import models
from soldiers.models import Soldier
from django_jalali.db import models as mod


# Create your models here.

class Sater(models.Model):
    sarbaz = models.ForeignKey(Soldier, on_delete=models.CASCADE, verbose_name='سرباز')
    date = mod.jDateTimeField(verbose_name='تاریخ ثبت ساتر')
    sub_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربرثبت کننده')
    sater_type = models.CharField(max_length=150, verbose_name='نوع ساتر', null=True)
    is_get = models.BooleanField(default=False, verbose_name='تایید ساتر')
