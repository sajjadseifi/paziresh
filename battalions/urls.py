from django.urls import path

from . import views

urlpatterns = [
    path('b/', views.MainViewBattalion.as_view(), name='all-Battalion'),
    path('b/create/', views.BattalionCreate.as_view(), name='BattalionCreate'),
    path('b/<int:pk>/update/', views.BattalionUpdate.as_view(), name='BattalionUpdate'),
    path('bg/', views.MainViewBattalionGroup.as_view(), name='MainViewBattalionGroup'),
    path('bg/create/', views.CreateBattalionGroup.as_view(), name='CreateBattalionGroup'),
    path('bg/<int:pk>/update/', views.BattalionUpdate.as_view(), name='BattalionUpdate'),

]
