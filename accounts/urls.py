from django.urls import path
from .views import *

from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login', user_login_page, name='login'),
    path('logout/', c_logout, name='logout'),
]
