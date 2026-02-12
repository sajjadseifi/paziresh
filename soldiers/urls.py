from django.urls import path
from .views import *

urlpatterns = [
    path('sarbaz/code/', paziresh_code_meli, name='sarbaz_codemeli'),
    path('sarbaz/<str:pk>', sabte_paziresh.as_view(), name='get_sarbaz'),
    path('sarbaz/p/<int:pk>', moarefi_be_gordan_va_sater.as_view(), name='moarefi_be_gordan_va_sater'),
    path('sarbaz/p/sater/<int:pk>', sater.as_view(), name='sater'),
    path('sarbaz/p/gordan/<int:pk>', moarefibegordan.as_view(), name='moarefibegordan'),
    path('sarbaz/create/', CreatePaziresh.as_view(), name='CreatePaziresh'),
    path('sarbaz/<str:pk>/update/', UpdatePaziresh.as_view(), name='updatePaziresh'),
    path('sarbaz/update/', UpdatePazireshPage.as_view(), name='updatePazireshpage'),
    path('sarbaz/all/', MainViewSoldires.as_view(), name='MainViewSoldires'),
    path('sarbaz/add_to_list_exel/', exel_add_to_db.as_view(), name='exel'),
    
    path('sarbaz/update_numbers/', exel_update_number.as_view(), name='exel_update_number'),
    path('export-excel/list_elame_hozor', export_to_excel_list_elame_hozor, name='export_to_excel_list_elame_hozor'),
    path('sarbaz/sater/group/', sater_group_print, name='sater_group_print'),
    path('sarbaz/moarefi/group/', moarefi_group_print, name='moarefi_begordan_group_print'),
    path('sarbaz/export_soldire_has_been_accepted_in_coures_all_data/',
         export_soldire_has_been_accepted_in_coures_all_data,
         name='export_soldire_has_been_accepted_in_coures_all_data'),
    path('sarbaz/export_soldire_has_been_accepted_all_data/data', export_soldire_has_been_accepted_all_data,
         name='export_soldire_has_been_accepted_all_data_'),
    path('sarbaz/update/update_db_from_exel_paziresh_hazer_bekhdmat',
         update_db_from_exel_paziresh_hazer_bekhdmat.as_view(),
         name='update_db_from_exel_paziresh_hazer_bekhdmat'),
    path('sarbaz/update/update_db_from_exel_paziresh_shode',
         update_db_from_exel_paziresh_shode.as_view(),
         name='update_db_from_exel_paziresh_shode'),
    path('soldire/search/paziresh/', MainViewSoldires.as_view(), name='soldier_search_paziresh'),
    path('export_to_excel_bdone_madrak_tahsili', export_to_excel_bdone_madrak_tahsili, name='export_to_excel_bdone_madrak_tahsili'),
    path(
         'excel_change_gharargah_sazandegi_khatam_true', 
          excel_change_gharargah_sazandegi_khatam_true, 
          name='excel_change_gharargah_sazandegi_khatam_true'
     ),
    path(
         'excel_change_gharargah_sazandegi_khatam_true_sample', 
         excel_change_gharargah_sazandegi_khatam_true_sample, 
         name='excel_change_gharargah_sazandegi_khatam_true_sample'
     ),
     #     
    path('mobilization/doc/view', mobilization_document_view, name='mobilization_document_view'),
    path('mobilization/doc/assign', mobilization_document_assign, name='mobilization_document_assign'),
    path('mobilization/doc/unassign', mobilization_document_unassign, name='mobilization_document_unassign'),
    path('mobilization/doc/upload', mobilization_document_upload, name='mobilization_document_upload'),
    path('mobilization/doc/delete', mobilization_document_delete, name='mobilization_document_delete'),

    path('api/rest/soldiers/',soldiers_rest_api,name='soldiers_rest_api')
]
