from django.db import models

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
