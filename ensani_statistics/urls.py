from django.urls import path

from .views import *

urlpatterns = [
    path('avalie', amar_avalie, name='amar'),
    path('gordanvgorhan', amar_gordan_gorhan, name='gordanvgorhan'),
    path('madraktahsili', amar_be_tafkik_madrk_tahsili, name='amar_be_tafkik_madrk_tahsili'),

]
