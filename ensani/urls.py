from django.urls import path
from . import views

urlpatterns = [
   path("amar-kol/", views.download_amar_kol, name="download_amar_kol"),
   path("shoro-dore/", views.download_shoro_dore, name="download_shoro_dore"),
   path("hezer/", views.download_hezer, name="download_hezer"),
   path("paziresh/", views.download_paziresh, name="download_paziresh"),
   path("yegan/", views.download_yegan, name="download_yegan"),
   path("tatbikh/", views.download_tatbikh, name="download_tatbikh"),
   path("download_kafiat/", views.download_kafiat, name="download_kafiat"),
   path("data/", views.data_app, name="data_app"),
]
