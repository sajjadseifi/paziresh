from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainViewBattalion.as_view(), name='all-Battalion'),

]
