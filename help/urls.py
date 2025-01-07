from django.urls import path
from . import views

urlpatterns = [
    path('download_import_rank_sample_excel/', views.download_import_rank_sample_excel,
         name='download_import_rank_sample_excel'),
    path('download_import_samane_sample_excel/', views.download_import_samane_sample_excel,
         name='download_import_samane_sample_excel'),
    path('download_import_number_sample_excel/', views.download_import_number_sample_excel,
         name='download_import_number_sample_excel'),
    path('download_import_jazbi_sample_excel/', views.download_import_jazbi_sample_excel,
         name='download_import_jazbi_sample_excel'),
    path('download_import_tatbigh_sample_excel/', views.download_import_tatbigh_sample_excel,
         name='download_import_tatbigh_sample_excel'),
    path('download_import_yegan_khdmati_sample_excel/', views.download_import_yegan_khdmati_sample_excel,
         name='download_import_yegan_khdmati_sample_excel'),
    path('download_import_bank_number_sample_excel/', views.download_import_bank_number_sample_excel,
         name='download_import_bank_number_sample_excel'),
]
