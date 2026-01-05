from django.contrib import admin
from .models import IdeologicalAssessment

@admin.register(IdeologicalAssessment)
class IdeologicalAssessmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'rank', 'created_at')
    list_filter = ('rank', 'created_at')
    search_fields = ('full_name', 'rank')
    ordering = ('-created_at',)

    fieldsets = (
        ('اطلاعات ارزیاب', {
            'fields': ('rank', 'full_name')
        }),
        ('اطلاعات سیستمی', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at',)
