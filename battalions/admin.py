from django.contrib import admin

# Register your models here.
from .models import battalion, battalion_group

admin.site.register(battalion)
admin.site.register(battalion_group)
