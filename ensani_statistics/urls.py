from django.urls import path

from .views import *

urlpatterns = [
    path('avalie', amar_avalie, name='amar'),
    path('gordanvgorhan', amar_gordan_gorhan, name='gordanvgorhan'),
    path('madraktahsili', amar_be_tafkik_madrk_tahsili, name='amar_be_tafkik_madrk_tahsili'),
    path('shorodore', amar_shoro_doreh, name='amar_shoro_doreh'),
    path('payandore', amar_payan_dore, name='amar_payan_dore'),
    path('amar_samane', amar_avalie_samane, name='amar_avalie_samane'),
    path('gozaresh_shoro_dore', gozaresh_shoro_dore, name='gozaresh_shoro_dore'),
    path('gozaresh_payan_dore', gozaresh_payan_dore, name='gozaresh_payan_dore'),
    path('gozaresh_yegan_khedmati', yegan_be_kar_girande, name='gozaresh_yegan_khedmati'),
    path('amare_yegan_bekar_girande_tabel', yegan_be_kar_girande_tabel, name='amare_yegan_bekar_girande_tabel'),
]
