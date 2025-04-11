from django.contrib import admin
from .models import Soldier


@admin.register(Soldier)
class SoldierAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'National_Code', 'Gordan', 'battalion_group', 'Date_of_dispatch', 'has_been_accepted', 'IsCheckout')
    search_fields = ('name', 'family', 'National_Code', 'phone_number', 'code_paziresh')
    list_filter = ('Amriye', 'has_been_accepted', 'IsCheckout', 'Gordan', 'battalion_group', 'province_name', 'marital_status')
    fieldsets = (
        ('اطلاعات فردی', {
            'fields': ('name', 'family', 'fathers_name', 'National_Code', 'Date_of_birth', 'place_of_birth',
                       'Religion', 'marital_status', 'phone_number', 'home_phone_number', 'Address', 'Place_of_Issue')
        }),
        ('تحصیلی و پزشکی', {
            'fields': ('Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
                       'physical_condition', 'Type_of_disease', 'health_insurance_card')
        }),
        ('اعزام و یگان', {
            'fields': ('Date_of_dispatch', 'Gordan', 'battalion_group', 'unit_name', 'unit_type',
                       'unit_address', 'unit_province', 'IsUnit')
        }),
        ('اطلاعات پذیرش', {
            'fields': ('has_been_accepted', 'acceptance_code', 'code_paziresh', 'code_gorhan',
                       'code_gorhan_nahai', 'tarikh_paziresh', 'date_improt_type')
        }),
        ('سوابق، امتیازات و نمرات', {
            'fields': ('discipline_score', 'basij_experience', 'council_experience', 'ideological_score',
                       'shooting_score', 'global_awards', 'national_awards', 'provincial_awards',
                       'global_articles', 'publications', 'quran_memorization', 'nahj_memorization',
                       'sajjadiya_memorization', 'battalion_activity', 'battalion_sample', 'top_three',
                       'basij_efficiency', 'total_score', 'rank')
        }),
        ('موارد متفرقه', {
            'fields': ('Sutter', 'bank_number', 'willing_to_learn', 'Amriye', 'Amriye_organization',
                       'Sufficiency_of_mobilization', 'the_medical_commission', 'Previous_service_record',
                       'attraction_of_the_organization', 'Successful_recruitment', 'Relative_to_inclusive',
                       'Relative_to_inclusive_number', 'IsCheckout', 'tatbigh', 'in_coures',
                       'tajdid_dore_moarefi_shode')
        }),
    )

    ordering = ('-tarikh_paziresh',)
