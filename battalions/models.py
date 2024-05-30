from django.db import models


# Create your models here.


class battalion(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام گردان')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    order = models.IntegerField(null=True, blank=True, verbose_name='اولویت مرتب سازی')

#
class battalion_group(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام گروهان')
    gordan = models.ForeignKey(battalion, on_delete=models.CASCADE, verbose_name='گردان')
    zirediplom = models.BooleanField(default=False, verbose_name='زیر دیپلم')
    diplom = models.BooleanField(default=False, verbose_name='دیپلم')
    ofghdiplom = models.BooleanField(default=False, verbose_name='فوق دیپلم')
    lisans = models.BooleanField(default=False, verbose_name='لیسانس')
    ofghlisans = models.BooleanField(default=False, verbose_name='فوق لیسانس')
    doctra = models.BooleanField(default=False, verbose_name='دکترا')
    shie = models.BooleanField(default=False, verbose_name='شیعه')
    ahle_tasnon = models.BooleanField(default=False, verbose_name='اهل تسنن')
    zarfiat = models.CharField(max_length=250, verbose_name='ظرفیت گروهان')
    takmilzarmit = models.BooleanField(default=False, verbose_name='تکمیل بودن ظرفیت')
    order = models.IntegerField(null=True, blank=True, verbose_name='اولویت مرتب سازی')
    salemm = models.BooleanField(default=False, verbose_name='سالم')
    moafazrazm = models.BooleanField(default=False, verbose_name='معاف ازرزم')
    gorehbe = models.BooleanField(default=False, verbose_name='گروه ب')
    moafazrazm_gorehbe = models.BooleanField(default=False, verbose_name='معاف از رزم + گروه ب')