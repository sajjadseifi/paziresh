from django.urls import path
from .views import *

urlpatterns = [
    path('sarbaz/', paziresh_code_meli, name='sarbaz_codemeli'),
    path('sarbaz/<int:pk>', sabte_paziresh.as_view(), name='get_sarbaz'),
    path('sarbaz/p/<int:pk>', moarefi_be_gordan.as_view(), name='moarefi_be_gordan'),
    path('sarbaz/sater/<int:pk>', sater.as_view(), name='sater'),
    path('sarbaz/create/', CreatePaziresh.as_view(), name='CreatePaziresh'),

]
