from django.urls import path
from .views import *

urlpatterns = [
    path('backup/', backup_database, name='backup_database'),
    path('backup/download', backup_database_download, name='backup_database_download'),
    path('restore/', restore_database, name='restore_database'),
]
