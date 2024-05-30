from django.db import models
from soldiers.models import Soldier


# Create your models here.


class NormalLetterModels(models.Model):
    letter_type = models.CharField(max_length=100, verbose_name='نوع نامه')
    # create_time =
    soldire = models.ForeignKey(Soldier, on_delete=models.CASCADE, verbose_name='سرباز')


class AmozeshLetterModels(models.Model):
    letter = models.ForeignKey(NormalLetterModels, on_delete=models.CASCADE, verbose_name='نامه')


