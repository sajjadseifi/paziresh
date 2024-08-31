from django.contrib import admin
from .models import Soldier


class SoldierAdmin(admin.ModelAdmin):
    # تعداد آیتم‌ها در هر صفحه
    list_per_page = 2000  # تعداد دلخواه خود را اینجا وارد کنید


admin.site.register(Soldier, SoldierAdmin)
