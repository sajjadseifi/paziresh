from django.db import models
from django_jalali.db import models as jmodels

class SlillTraining(models.Model):
    title = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        verbose_name="عنوان مهارت"
    )
    code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="کد مهارت"
    )
    category = models.CharField(
        max_length=255,
        verbose_name="دسته‌بندی مهارت"
    )

    class Meta:
        verbose_name = "مهارت"
        verbose_name_plural = "مهارت‌ها"

    def __str__(self):
        return f"{self.title} ({self.category})"

from django.db import models

class HazardSettings(models.Model):
    # فیلدهای جدول گواهی مخاطرات
    letter_number = models.CharField(max_length=100, verbose_name="شماره نامه")
    year = models.PositiveSmallIntegerField(verbose_name="سال", blank=True, null=True)
    month_name = models.CharField(max_length=20, verbose_name="ماه به حروف", blank=True, null=True)
    first_aid_hours = models.PositiveSmallIntegerField(default=22, verbose_name="ساعت کمک‌های اولیه")
    hazard_preparedness_hours = models.PositiveSmallIntegerField(default=8, verbose_name="ساعت آمادگی در برابر مخاطرات")
    certificate_date = models.DateField(verbose_name="تاریخ گواهی")
    start_date = models.DateField(verbose_name="تاریخ شروع دوره")
    end_date = models.DateField(verbose_name="تاریخ پایان دوره")
    province = models.CharField(max_length=20, verbose_name="استان محل آموزش", blank=True, null=True)
    city = models.CharField(max_length=20, verbose_name="شهر محل آموزش", blank=True, null=True)

    def __str__(self):
        return f"تنظیمات مخاطرات ({self.letter_number})"

    class Meta:
        verbose_name = "تنظیمات مخاطرات"
        verbose_name_plural = "تنظیمات مخاطرات"

from django.db import models

class TechnicalVocational(models.Model):
    name = models.CharField(max_length=255,verbose_name="نام رشته")
    code = models.CharField(max_length=100,unique=True,verbose_name="کد رشته")
    created_at = models.DateTimeField( auto_now_add=True,verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField( auto_now=True,verbose_name="تاریخ بروزرسانی")

    class Meta:
        db_table = 'technical_vocational_fields'
        verbose_name = "رشته فنی و حرفه‌ای"
        verbose_name_plural = "رشته‌های فنی و حرفه‌ای"
        ordering = ['code']
        constraints = [
            models.UniqueConstraint(fields=['name', 'code'], name='unique_name_code')
        ]
    def __str__(self):
        return f"{self.name} ({self.code})"
