from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class ApplicationValues(Enum):
    RANK_SCORES = "نمره درجات"
    # RANK_SCORES_ADD = "افزودن - نمره درجات"
    # RANK_SCORES_EDIT = "ویرایش - نمره درجات"
    # RANK_SCORES_DELETE = "حذف - نمره درجات"

    SKILL_MANAGEMENT = "مهارت آموزی"
    # SKILL_MANAGEMENT_ADD = "افزودن - مهارت آموزی"
    # SKILL_MANAGEMENT_EDIT = "ویرایش - مهارت آموزی"
    # SKILL_MANAGEMENT_DELETE = "حذف - مهارت آموزی"

    COURSE = "سازماندهی سرباز"
    # COURSE_ADD = "افزودن   سازماندهی سرباز"
    # COURSE_EDIT = "ویرایش   سازماندهی سرباز"
    # COURSE_DELETE = "حذف - سازماندهی سرباز"
     
    SOLDIER_PROBLEMS = "مشکلات سربازان"
    # SOLDIER_PROBLEMS_ADD = "افزودن - مشکلات سربازان"
    # SOLDIER_PROBLEMS_EDIT = "ویرایش - مشکلات سربازان"
    # SOLDIER_PROBLEMS_DELETE = "حذف - مشکلات سربازان"
    
    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]

class DepartmentValues(Enum):
    FARMANDEHI = "فرماندهی"
    NIRU_ENSANI = "نیرو انسانی"
    AQIDATI = "عقیدتی"
    GORDAN = "گردان"
    GOROHAN = "گروهان"
    BEHDARI = "بهداری"
    AMOOZESH = "آموزش"
    FAVA = "فاوا"
    AMAD = "آماد"
    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]


class AccessName(Enum):
    # 👥 سربازان
    SOLDIERS = "سربازان"
    GORDAN_SOLDIERS = "سربازان گردان"
    GROHAN_SOLDIERS = "سربازان گروهان"
    # 🧩 سایر دسترسی‌ها
    APPLICATIONS = "برنامه‌ها"
    LETTERS = "نامه‌ها"
    DEPARTMENTS='واحد ها'
    @classmethod
    def choices(cls):
        """برمی‌گرداند تا بتوان در مدل استفاده کرد."""
        return [(tag.name, tag.value) for tag in cls]

class UserAccess(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accesses",
        verbose_name="کاربر"
    )
    access_name = models.CharField(
        max_length=50,
        choices=AccessName.choices(),
        verbose_name="نام دسترسی"
    )

    # مقدار دسترسی — می‌تواند عدد، رشته یا "همه" باشد
    access_value = models.CharField(
        max_length=100,
        verbose_name="مقدار دسترسی",
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('user', 'access_name', 'access_value')
        verbose_name = "دسترسی کاربر"
        verbose_name_plural = "دسترسی‌های کاربران"

    def __str__(self):
        return f"{self.user.username} - {self.get_access_name_display()} ({self.access_value})"
