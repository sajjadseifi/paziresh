from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ensani_backup.forms import BackupUploadForm
from ensaniapp_settings.models import EnsaniSettings 
import io
from django.http import HttpResponse
from django.utils import timezone
import jdatetime 
from django.contrib.auth.decorators import login_required
import shutil
from pathlib import Path

# مسیر فولدر بکاپ‌ها
base_dir = Path(__file__).resolve().parent.parent
backups_dir = base_dir / "@bacckups"
history_backups_dir = backups_dir / "history"

@login_required
def backup_database_download(request):
    path = request.GET.get('path')
    db_path = base_dir / path
    
    if db_path.exists():
        backup_filename = db_path.name 
        with open(db_path, 'rb') as f:
            file_data = f.read()

        # ساخت فایل در حافظه موقت
        buffer = io.BytesIO()
        buffer.write(file_data)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'

        return response

    response = HttpResponse("File not found.", content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="ناموجود.txt"'
    return response

@login_required
def backup_database(request):
    # مسیر دیتابیس SQLite
    db_path = Path('db.sqlite3')

    # ایجاد نام فایل بکاپ با توجه به زمان
    en = EnsaniSettings.objects.first()
    dore = en.shomare_dore
    time = jdatetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    backup_filename = f'backup__{dore}__{time}.sqlite3'
   # --- مرحله 1: ذخیره در فولدر history ---
    # if db_path.exists():
    #     backup_path = history_backups_dir / backup_filename
    #     shutil.copy2(db_path, backup_path)  # کپی سریع دیتابیس با حفظ timestamp

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


@login_required
def restore_database(request):
 
    backups = []
    history_backups = []
    
    if request.method == 'POST':
        form = BackupUploadForm(request.POST, request.FILES)
        if form.is_valid():
            backup_file = request.FILES['backup_file']
            # مسیر دیتابیس اصلی
            db_path = Path('db.sqlite3')

            # --- مرحله 1: بکاپ گرفتن از دیتابیس فعلی ---
            if db_path.exists():
                en = EnsaniSettings.objects.first()
                dore = en.shomare_dore
                time_str = jdatetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
                backup_filename = f'backup__{dore}__{time_str}.sqlite3'

                # مسیر نهایی فایل بکاپ در history
                backup_path = history_backups_dir / backup_filename

 
                if db_path.exists():
                    backup_path = history_backups_dir / backup_filename
                    shutil.copy2(db_path, backup_path)  # کپی سریع دیتابیس با حفظ timestamp

            # --- مرحله 2: بازگردانی فایل آپلود شده ---
            with open(db_path, 'wb') as f:
                for chunk in backup_file.chunks():
                    f.write(chunk)

            return HttpResponse('پایگاه داده با موفقیت بازگردانی شد.')
    else:
        form = BackupUploadForm()
 
    if backups_dir.exists():
        for f in backups_dir.glob("*.sqlite3"):
            time_str = jdatetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%H-%M-%S__%Y-%m-%d")
            
            backups.append({
                'name': f.stem,  
                'ext': f.suffix,      
                'size': f.stat().st_size,
                'size_kb': round(f.stat().st_size / 1024, 2),
                'modified': time_str,
                'path':f"@bacckups/${f.name}"
                
            })
    
    if history_backups_dir.exists():
        for f in history_backups_dir.glob("*.sqlite3"):
            time_str = jdatetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%H-%M-%S__%Y-%m-%d")

            history_backups.append({
                'name': f.stem,       # نام فایل بدون پسوند
                'ext': f.suffix,      # پسوند فایل، مثلاً '.sqlite3'
                'size': f.stat().st_size,      # حجم فایل به بایت
                'size_kb': round(f.stat().st_size / 1024, 2),
                'modified': time_str, # timestamp آخرین تغییر
                'path':f"@bacckups/history/{f.name}"
                
            })

    return render(request, 'ensani_backup/restore.html', {'form': form,'backups':backups,'history_backups':history_backups})
