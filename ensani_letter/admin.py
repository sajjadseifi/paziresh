from django.contrib import admin
from .models import NormalLetterModels, CheckoutLetterModels

# Register your models here.
admin.site.register(NormalLetterModels)
admin.site.register(CheckoutLetterModels)
