from django.contrib import admin
from .models import HazardSettings,SlillTraining,TechnicalVocational

@admin.register(SlillTraining)
class SlillTrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'code', 'category')
    ordering = ('category', 'title')
    list_per_page = 25

@admin.register(HazardSettings)
class HazardSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'letter_number',
        'year',
        'month_name',
        'certificate_date',
        'start_date',
        'end_date',
        'province',
        'city',
    )

    list_filter = ('year', 'month_name')
    search_fields = ('letter_number',)

    fieldsets = (
        ("اطلاعات نامه", {
            'fields': ('letter_number', 'year', 'month_name','province','city')
        }),
        ("ساعات آموزشی", {
            'fields': ('first_aid_hours', 'hazard_preparedness_hours')
        }),
        ("تاریخ‌ها", {
            'fields': ('certificate_date', 'start_date', 'end_date')
        }),
        
    )


@admin.register(TechnicalVocational)
class TechnicalVocationalAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    ordering = ('code',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 30
