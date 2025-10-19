from django.urls import path
from . import views

app_name = "skills"

urlpatterns = [
    path("", views.index, name="index"),                 # صفحه اصلی مهارت‌آموزی
    path("list/", views.skill_list, name="list"),        # لیست مهارت‌ها
    path("actions/", views.skills_actions, name="actions"),  # عملیات ها
    path("assign/", views.assign_view, name="assign"),  # تخصیص مهارت به سرباز مهارت‌ها
    path("assign/manual", views.assign_create_manual, name="assign_create_manual"),  # تخصیص مهارت به سرباز مهارت‌ها
    path("assign/upload/excel", views.assign_view, name="assign_upload_excel"),  # تخصیص مهارت به سرباز مهارت‌ها
    path("technical-vocational/", views.technical_vocational_page, name="technical_vocational"),        # لیست مهارت‌ها
    path('technical-vocational/create/', views.technical_vocational_create, name='technical_vocational_create'),
    path('technical-vocational/<int:pk>/update/', views.technical_vocational_update, name='technical_vocational_update'),
    path('technical-vocational/<int:pk>/delete/', views.technical_vocational_delete, name='technical_vocational_delete'),
    path('technical-vocational/exam/soldier', views.technical_vocational_add_soldier, name='technical_vocational_add_soldier'),
    path('technical-vocational/exam/soldier/eazy', views.technical_vocational_eazy_register, name='technical_vocational_eazy_register'),
    path('technical-vocational/export/excel/', views.technical_vocational_soldiers_export_excel, name='technical_vocational_export_excel'),
    path('technical-vocational/export/zip/', views.technical_vocational_soldiers_export_zip, name='technical_vocational_export_zip'),

    path("create/", views.skill_create, name="create"),  # ایجاد مهارت جدید
    path("categories/", views.categories, name="categories"),  # دسته‌بندی مهارت‌ها
    path("<int:pk>/", views.skill_detail, name="detail"),       # جزئیات یک مهارت
    path("actions/", views.skill_create, name="actions"),  # ایجاد مهارت جدید
    path("download-sample/", views.download_sample_excel, name="download_sample_excel"),
    path("create/manual/", views.create_manual, name="create_manual"),
    path("create/excel/", views.create_excel, name="create_excel"),
    path("create/excel/stream", views.create_excel_stream, name="create_excel_stream"),
    path("export/skills/excel/", views.export_skills_excel, name="export_skills_excel"),
    path("export/assign/excel//<str:mode>/", views.assign_soldier_skills_excel, name="export_assign_excel"),
    path("certificates/hazard", views.CreateOrUpdateHazardSettings.as_view(), name="certificates_hazard"),
    path("certificates/hazard/print", views.certificates_hazard_print, name="certificates_hazard_print"),
]
