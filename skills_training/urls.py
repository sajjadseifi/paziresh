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
