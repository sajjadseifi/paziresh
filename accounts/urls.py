from django.urls import path
from .views import *

from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login', user_login_page, name='login'),
    path('logout/', c_logout, name='logout'),
    path('account/access', account_access, name='account_access'),
    path('account/form/details/', user_details_form, name='user_details_form'),
    path('account/form/user/new', create_new_user_form, name='create_new_user_form'),
    path('account/form/user/change-password', user_change_password_form, name='user_change_password_form'),
    path('account/form/access/soldiers', soldiers_access_form, name='soldiers_access_form'),
    path('account/form/access/application', application_access_form, name='application_access_form'),
    path('account/access/403', account_access_403, name='account_access_403'),
]