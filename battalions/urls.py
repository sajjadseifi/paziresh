from django.urls import path

from . import views

urlpatterns = [
    path('b/', views.MainViewBattalion.as_view(), name='all-Battalion'),
    path('b/create/', views.BattalionCreate.as_view(), name='BattalionCreate'),
    path('b/<int:pk>/update/', views.BattalionUpdate.as_view(), name='BattalionUpdate'),
    path('bg/', views.MainViewBattalionGroup.as_view(), name='MainViewBattalionGroup'),
    path('bg/create/', views.CreateBattalionGroup.as_view(), name='CreateBattalionGroup'),
    path('bg/<int:pk>/update/', views.BattalionGroupUpdate.as_view(), name='BattalionGroupUpdate'),
    path('bg/<int:battalation_pk>/batch/add', views.add_battalion_group_batch, name='add_battalion_group_batch'),
    path('bg/<int:pk>/batch/remove', views.remove_battalion_group_batch, name='remove_battalion_group_batch'),
    path('bg/<int:battalation_pk>/batch/remove/all', views.remove_all_battalion_group_batch, name='remove_all_battalion_group_batch'),
    path('bg/<int:battalation_pk>/batch/save', views.save_battalion_group_batch, name='save_battalion_group_batch'),

]

