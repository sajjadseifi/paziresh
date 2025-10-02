from django.urls import path

from .views import *

urlpatterns = [
    path('avalie', amar_avalie, name='amar'),
    path('gordanvgorhan', amar_gordan_gorhan, name='gordanvgorhan'),
    path('madraktahsili', amar_be_tafkik_madrk_tahsili, name='amar_be_tafkik_madrk_tahsili'),
    path('shorodore', amar_shoro_doreh, name='amar_shoro_doreh'),
    path('payandore', amar_payan_dore, name='amar_payan_dore'),
    path('amar_samane', amar_avalie_samane, name='amar_avalie_samane'),
    path('samane_baghimonde', amar_avalie_samane_baghimonde, name='amar_avalie_samane_baghimonde'),
    path('amar_avalie_samane_paziresh_shode', amar_avalie_samane_paziresh_shode, name='amar_avalie_samane_paziresh_shode'),
    path('gozaresh_shoro_dore', gozaresh_shoro_dore, name='gozaresh_shoro_dore'),
    path('gozaresh_payan_dore', gozaresh_payan_dore, name='gozaresh_payan_dore'),
    path('gozaresh_yegan_khedmati', yegan_be_kar_girande, name='gozaresh_yegan_khedmati'),
    path('amare_yegan_bekar_girande_tabel', yegan_be_kar_girande_tabel, name='amare_yegan_bekar_girande_tabel'),
    path('amara_rank', amar_rank, name='amar_rank'),
    path('amara_rank/gardeshkar/download', generate_gardesh_kar, name='generate_gardesh_kar'),
    path('amara_rank/gardeshkar', create_rank_gardesh_kar, name='create_rank_gardesh_kar'),
    path('physical/stats/', physical_stats_view, name='physical_stats'),
    path('physical/table/', physical_table_view, name='physical_table'),
    path('physical/height_weight_chart/', height_weight_chart_view, name='physical_height_weight_chart'),
    path('physical/bmi_chart/', bmi_chart_view, name='physical_bmi_chart'),
]
