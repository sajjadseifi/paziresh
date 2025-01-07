import os
from django.http import FileResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required
def download_import_rank_sample_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'help', 'file', 'exel', 'import_rank_sample.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='import_rank_sample.xlsx')

@login_required
def download_import_samane_sample_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'help', 'file', 'exel', 'import_samane_sample.xls')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='import_samane_sample.xls')

@login_required
def download_import_number_sample_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'help', 'file', 'exel', 'import_number.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='import_number.xlsx')

@login_required
def download_import_jazbi_sample_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'help', 'file', 'exel', 'import_zajbi_sample.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='import_zajbi_sample.xlsx')


@login_required
def download_import_tatbigh_sample_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'help', 'file', 'exel', 'impot_tatbigh_sample.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='impot_tatbigh_sample.xlsx')

@login_required
def download_import_yegan_khdmati_sample_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'help', 'file', 'exel', 'import_yegan_khdmati_sample.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='import_yegan_khdmati_sample.xlsx')

@login_required
def download_import_bank_number_sample_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'help', 'file', 'exel', 'import_bank_number_sample.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='import_bank_number_sample.xlsx')