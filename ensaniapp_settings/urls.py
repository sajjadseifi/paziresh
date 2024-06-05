from django.urls import path
from .views import *

urlpatterns = [
    # path('sarbaz/code/', paziresh_code_meli, name='sarbaz_codemeli'),
    path('settings/', CreateOrUpdateSettings.as_view(), name='CreateOrUpdateSettings'),

]
