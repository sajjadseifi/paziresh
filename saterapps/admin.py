from django.contrib import admin

# Register your models here.
from .models import Sater

class SaterAdmin(admin.ModelAdmin):
    search_fields = ['sarbaz__National_Code']

admin.site.register(Sater,SaterAdmin)
