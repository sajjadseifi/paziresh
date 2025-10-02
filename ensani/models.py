from django.db import models
from django.utils import timezone


class ActivityLog(models.Model):
    class NoteType(models.TextChoices):
        USER = "user", "کاربر"
        SOLDIER = "soldier", "سرباز"
        LETTER = "letter", "نامه"
        SYSTEM = "system", "سیستم"
        SATER = "sater", "ساتر"
        DTABASE = "database", "پایگاه داده"

    class Action(models.TextChoices):
        CREATE = "create", "ایجاد"
        PRINT = "print", "پرینت"
        UPDATE = "update", "بروزرسانی"
        DELETE = "delete", "حذف"
        STATUS_CHANGE = "status_change", "تغییر وضعیت"

    note_type = models.CharField(
        max_length=50,
        choices=NoteType.choices,
        verbose_name="نوع یادداشت"
    )
    action = models.CharField(
        max_length=50,
        choices=Action.choices,
        verbose_name="عملیات"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="توضیحات"
    )
    created_at = models.DateTimeField(default=timezone.now) 


    class Meta:
        ordering = ["-created_at"]
        verbose_name = "یادداشت فعالیت"
        verbose_name_plural = "یادداشت‌های فعالیت"

    def __str__(self):
        return f"{self.get_note_type_display()} | {self.get_action_display()}"

    def to_dict(self):
        return {
            "id": self.id,
            "note_type": self.get_note_type_display(),
            "action": self.get_action_display(),
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }


