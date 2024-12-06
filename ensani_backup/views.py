from django.shortcuts import render
from ensani_backup.forms import BackupUploadForm
import io
from django.http import HttpResponse
from django.utils import timezone


def backup_database(request):
    # مسیر دیتابیس SQLite
    db_path = 'db.sqlite3'

    # ایجاد نام فایل بکاپ با توجه به زمان
    backup_filename = f'backup_{timezone.now().strftime("%Y-%m-%d_%H-%M-%S")}.sqlite3'

    # خواندن دیتابیس به صورت in-memory
    with open(db_path, 'rb') as f:
        file_data = f.read()

    # ساخت فایل در حافظه موقت
    buffer = io.BytesIO()
    buffer.write(file_data)
    buffer.seek(0)

    # ایجاد پاسخ برای دانلود فایل بکاپ
    response = HttpResponse(buffer, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'

    return response


def restore_database(request):
    if request.method == 'POST':
        form = BackupUploadForm(request.POST, request.FILES)
        if form.is_valid():
            backup_file = request.FILES['backup_file']

            # مسیر دیتابیس اصلی
            db_path = 'db.sqlite3'

            # ذخیره فایل بکاپ به عنوان دیتابیس اصلی
            with open(db_path, 'wb') as f:
                for chunk in backup_file.chunks():
                    f.write(chunk)

            return HttpResponse('Database restored successfully.')

    else:
        form = BackupUploadForm()

    return render(request, 'ensani_backup/restore.html', {'form': form})
