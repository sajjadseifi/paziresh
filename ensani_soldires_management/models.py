from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from soldiers.models import Soldier
class IdeologicalAssessment(models.Model):
    class Meta:
        verbose_name = 'ارزیاب'
        verbose_name_plural = 'ارزیاب‌ها'

    full_name = models.CharField('نام و نام خانوادگی', max_length=100)
    rank = models.CharField('درجه', max_length=50)
    created_at = models.DateTimeField('تاریخ ثبت', auto_now_add=True)


    def __str__(self):
        return f"{self.rank} {self.full_name}".strip()

class SoldierTrainingRecord(models.Model):
    EDITABLE_FIELDS = [
        'shooting_stage_1',
        'shooting_stage_2',
        'shooting_stage_3',
        'shooting_stage_4',
        'tactic_score',
        'physical_fitness_score',
        'military_discipline_score',
    ]

    READONLY_FIELDS = [
        'shooting_avg',
        'final_average',
    ]
    WEAPON_TYPE = 'کلاشنیکف'
    @classmethod
    def training_fields(cls):
        orders = [
            'shooting_stage_1',
            'shooting_stage_2',
            'shooting_stage_3',
            'shooting_stage_4',
            'shooting_avg',
            'weapon_type',
            'tactic_score',
            'physical_fitness_score',
            'military_discipline_score',
            'final_average'
        ]

        fields = []
        for f in orders:
            if f in cls.EDITABLE_FIELDS:
                fields.append({'field': f, 'readonly': False})
            elif f in cls.READONLY_FIELDS:
                fields.append({'field': f, 'readonly': True})
            elif f == 'weapon_type':
                fields.append({'field': f, 'static': True, 'value': cls.WEAPON_TYPE})
        return fields
    
    soldier = models.OneToOneField(
        Soldier,
        on_delete=models.CASCADE,
        related_name='training_record',
        verbose_name='سرباز'
    )

    # تیراندازی
    shooting_stage_1 = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='تیراندازی مرحله اول'
    )
    shooting_stage_2 = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='تیراندازی مرحله دوم'
    )
    shooting_stage_3 = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='تیراندازی مرحله سوم'
    )
    shooting_stage_4 = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='تیراندازی مرحله چهارم'
    )

    shooting_avg = models.FloatField(
        null=True, blank=True,
        verbose_name='معدل تیراندازی'
    )

    # سایر نمرات
    tactic_score = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='نمره تاکتیک'
    )
    physical_fitness_score = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='نمره آمادگی جسمانی'
    )
    military_discipline_score = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='نمره آداب نظامی'
    )

    final_average = models.FloatField(
        null=True, blank=True,
        verbose_name='معدل کل'
    )

    # ---------- توابع محاسباتی ----------

    def calculate_shooting_avg(self):
        scores = [
            self.shooting_stage_1,
            self.shooting_stage_2,
            self.shooting_stage_3,
            self.shooting_stage_4,
        ]
        valid_scores = [s for s in scores if s is not None]

        if not valid_scores:
            return None

        avg = sum(valid_scores) / len(valid_scores)
        return float(
            Decimal(avg).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        )

    def calculate_final_average(self):
        scores = [
            self.shooting_avg,
            self.tactic_score,
            self.physical_fitness_score,
            self.military_discipline_score,
        ]

        if any(s is None for s in scores):
            return None

        avg = sum(scores) / 4
        return float(
            Decimal(avg).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        )

    def save(self, *args, **kwargs):
        self.shooting_avg = self.calculate_shooting_avg()
        self.final_average = self.calculate_final_average()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'کارنامه آموزش'
        verbose_name_plural = 'کارنامه‌های آموزش'

    def __str__(self):
        return f'کارنامه آموزش {self.soldier}'
