from django.db import models
from soldiers.models import Soldier
from django_jalali.db import models as jmodels

class LetterType(models.TextChoices):
    NORMAL = "normal", "نامه عادی"
    CHECKOUT = "checkout", "نامه تسویه حساب"
    RUNAWAY = "runaway", "نامه فرار"
    FARAJA = "faraja", "نامه فراجا"
    MOAREFI = "moarefi", "نامه معرفی"
    REGISTER = "register", "نامه گواهی عضویت"
    
class NormalLetterModels(models.Model):
    subject = models.CharField(max_length=100, verbose_name='موضوع نامه')
    soldire = models.ForeignKey(Soldier, on_delete=models.CASCADE, verbose_name='سرباز')
    create_time = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ')
    destination = models.CharField(max_length=150, verbose_name='مقصد نامه', null=True, blank=True)
    description = models.CharField(max_length=150, verbose_name='توضیحات', null=True, blank=True)
    number = models.CharField(max_length=200, verbose_name='شماره نامه', null=True, blank=True)
    status = models.CharField(max_length=200, verbose_name='وضعیت', null=True, blank=True)
    
    parent_letter_number = models.CharField(max_length=200, verbose_name='بازگشت به شماره نامه', null=True, blank=True)
    parent_letter_type = models.CharField(
        max_length=20,
        choices=LetterType.choices,
        null=True,
        blank=True,
        verbose_name="نوع نامه والد"
    )
    
    class Meta:
        verbose_name = "نامه عادی"
        verbose_name_plural = "نامه‌های عادی"

    def __str__(self):
        return f"{self.soldire}"


class CheckoutLetterModels(models.Model):
    create_time = jmodels.jDateTimeField(null=True, blank=True, verbose_name='تاریخ')
    soldire = models.ForeignKey(Soldier, on_delete=models.CASCADE, verbose_name='سرباز')
    description = models.CharField(max_length=150, verbose_name='توضیحات', null=True, blank=True)
    number = models.CharField(max_length=250, verbose_name='شماره نامه')
    c_type = models.CharField(max_length=250, verbose_name='علت تسویه حساب')
    status = models.CharField(max_length=200, verbose_name='وضعیت', null=True, blank=True)

    def __str__(self):
        return f"{self.soldire} - {self.c_type} - {self.status}"

    class Meta:
        verbose_name = "نامه تسویه حساب"
        verbose_name_plural = "نامه‌های تسویه حساب"

    def __str__(self):
        return f"{self.soldire}"


class RegisterNormalLetter(models.Model):
    in_come_letter_numbers = models.CharField(max_length=100, verbose_name='شماره نامه وارده', null=True, blank=True)
    in_come_letter_data = models.CharField(max_length=100, verbose_name='تاریخ نامه وارده', null=True, blank=True)
    in_come_submit_locations = models.CharField(max_length=100, verbose_name='مبدا صادر کننده', null=True, blank=True)
    normal_letter = models.ForeignKey(NormalLetterModels, on_delete=models.CASCADE, verbose_name='نامه عادی')

    def __str__(self):
        return f"{self.in_come_letter_numbers} - {self.in_come_letter_data}"

    class Meta:
        verbose_name = "نامه گواهی عضویت"
        verbose_name_plural = "نامه‌های گواهی عضویت"


class RunawayNormallLetter(models.Model):
    type = models.CharField(max_length=120, verbose_name='دلیل فرار', null=True, blank=True)
    run_away_dated = models.CharField(max_length=120, verbose_name='تاریخ فرار', null=True, blank=True)
    normal_letter = models.ForeignKey(NormalLetterModels, on_delete=models.CASCADE, verbose_name='نامه عادی')

    def __str__(self):
        return f"نامه فرار"

    class Meta:
        verbose_name = "نامه فرار"
        verbose_name_plural = "نامه‌های فرار"


class FarajaNormallLetter(models.Model):
    faraja_leter_number = models.CharField(max_length=120, verbose_name='شماره نامه فراجا', null=True, blank=True)
    faraja_leter_date = models.CharField(max_length=120, verbose_name='دلیل فرار', null=True, blank=True)
    elat = models.CharField(max_length=120, verbose_name='تاریخ نامه فراجا', null=True, blank=True)
    normal_letter = models.ForeignKey(NormalLetterModels, on_delete=models.CASCADE, verbose_name='نامه عادی', null=True,
                                      blank=True)

    def __str__(self):
        return f"نامه فراجا"

    class Meta:
        verbose_name = "نامه فراجا"
        verbose_name_plural = "نامه‌های فراجا"


class MoarefiNormallLetter(models.Model):
    tarikh_moarefi = models.CharField(max_length=120, verbose_name='تاریخ معرفی', null=True, blank=True)
    destination = models.CharField(max_length=250, verbose_name='مقصد نامه', null=True, blank=True)
    no_moarefi = models.CharField(max_length=250, verbose_name='به علت', null=True, blank=True)
    normal_letter = models.ForeignKey(NormalLetterModels, on_delete=models.CASCADE, verbose_name='نامه عادی', null=True,
                                      blank=True)
    sater = models.CharField(max_length=100, verbose_name='ساتر', null=True, blank=True)

    def __str__(self):
        return f"معرفی نامه"

    class Meta:
        verbose_name = "نامه معرفی"
        verbose_name_plural = "نامه‌های معرفی"



class RawLetter(models.Model):
    # ========================
    # اطلاعات سرباز
    # ========================
    soldier_name = models.CharField(null=True, blank=True, max_length=100, verbose_name="نام سرباز")
    soldier_family = models.CharField(null=True, blank=True, max_length=100, verbose_name="نام خانوادگی سرباز")
    soldier_fathers_name = models.CharField(null=True, blank=True, max_length=100, verbose_name="نام پدر سرباز")
    soldier_national_code = models.CharField(null=True, blank=True, max_length=20, verbose_name="کد ملی سرباز")
    soldier_acceptance_code = models.IntegerField(null=True, blank=True, verbose_name="کد پذیرش سرباز")
    soldier_date_of_dispatch = models.CharField(null=True, blank=True, max_length=100, verbose_name="تاریخ اعزام سرباز")

    # ========================
    # اطلاعات کلی نامه
    # ========================
    title = models.CharField(max_length=200, verbose_name="عنوان نامه", null=True, blank=True)
    letter_type = models.CharField(
        max_length=20,
        choices=LetterType.choices,
        default=('other', 'سایر') ,
        verbose_name="نوع نامه",
    )
    number = models.CharField(max_length=100, verbose_name="شماره نامه", null=True, blank=True)
    return_to_number = models.CharField(max_length=100, verbose_name="بازگشت به شماره نامه", null=True, blank=True)
    date = jmodels.jDateTimeField(null=True, blank=True, verbose_name="تاریخ نامه")
    destination = models.CharField(max_length=200, verbose_name="گیرنده/مقصد", null=True, blank=True)
    description = models.TextField(verbose_name="متن/توضیحات", null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name="وضعیت", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "نامه خام"
        verbose_name_plural = "نامه‌های خام"

    def __str__(self):
        return f"{self.title or 'نامه بدون عنوان'} - {self.get_letter_type_display()}"
