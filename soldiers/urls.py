from django.urls import path
from .views import *

urlpatterns = [
    path('sarbaz/code/', paziresh_code_meli, name='sarbaz_codemeli'),
    path('sarbaz/<str:pk>', sabte_paziresh.as_view(), name='get_sarbaz'),
    path('sarbaz/p/<int:pk>', moarefi_be_gordan_va_sater.as_view(), name='moarefi_be_gordan_va_sater'),
    path('sarbaz/p/sater/<int:pk>', sater.as_view(), name='sater'),
    path('sarbaz/p/gordan/<int:pk>', moarefi_be_gordan_va_sater.as_view(), name='moarefi_be_gordan_va_sater'),
    path('sarbaz/create/', CreatePaziresh.as_view(), name='CreatePaziresh'),
    path('sarbaz/<str:pk>/update/', UpdatePaziresh.as_view(), name='updatePaziresh'),
    path('sarbaz/update/', UpdatePazireshPage.as_view(), name='updatePazireshpage'),
    path('sarbaz/all/', MainViewSoldires.as_view(), name='MainViewSoldires'),
    path('sarbaz/add_to_list_exel/', exel_add_to_db.as_view(), name='exel'),

]
