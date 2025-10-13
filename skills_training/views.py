from django.shortcuts import render, get_object_or_404
from .models import SlillTraining
from soldiers.models import Soldier
from django.db.models import Count, Q
from django.contrib import messages
from django.shortcuts import redirect, render
import openpyxl
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import SlillTraining
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
import urllib.parse
import jdatetime

from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

template_pages = 'pages'

@login_required
def index(request):
    # ✅ تعداد کل مهارت‌ها
    total_skills = SlillTraining.objects.count()
    total_soldiers = Soldier.objects.count() or 1  # جلوگیری از تقسیم بر صفر

    # ✅ تعداد دسته‌های منحصربه‌فرد (بدون خالی‌ها)
    total_categories = (
        SlillTraining.objects
        .exclude(category__isnull=True)
        .exclude(category__exact='')
        .values('category')
        .distinct()
        .count()
    )

    # ✅ تعداد مهارت‌هایی که کد ندارند
    skills_without_code = SlillTraining.objects.filter(
        Q(code__isnull=True) | Q(code__exact='')
    ).count()

    # ✅ تعداد سربازانی که حداقل یکی از دو مهارت را دارند
    soldiers_with_skills = Soldier.objects.filter(
        Q(skill_1__isnull=False) | Q(skill_2__isnull=False)
    ).distinct().count()


    # ✅ ۵ مهارت پر استفاده با درصد استفاده از کل سربازان
    skills_usage = (
        SlillTraining.objects
        .annotate(
            usage_count=Count('primary_soldiers', distinct=True) + Count('secondary_soldiers', distinct=True)
        )
        .annotate(
            usage_percent=(100.0 * (
                Count('primary_soldiers', distinct=True) + Count('secondary_soldiers', distinct=True)
            ) / total_soldiers)
        )
        .order_by('-usage_count')[:6]
    )

    # ✅ محاسبه آمار دسته‌ها (تعداد مهارت و سربازان مرتبط)
    # برای جلوگیری از N+1 Query از annotate و Subquery استفاده می‌کنیم
    categories_qs = (
        SlillTraining.objects
        .exclude(category__isnull=True)
        .exclude(category__exact='')
        .values('category')
        .annotate(
            skill_count=Count('id', distinct=True),
            soldiers_count=Count('primary_soldiers', distinct=True) + Count('secondary_soldiers', distinct=True)
        )
        .order_by('category')
    )

    # تبدیل به لیست ساده‌تر برای ارسال به قالب
    categories_info = list(categories_qs)

    # ✅ ارسال تمام داده‌ها به تمپلیت داشبورد
    return render(request, f"{template_pages}/index.html", {
        "total_skills": total_skills,
        "total_categories": total_categories,
        "skills_without_code": skills_without_code,
        "soldiers_with_skills": soldiers_with_skills,
        "top_skills": skills_usage,
        "categories_info": categories_info,
    })

    
    
def skill_list(request):
    # همه مهارت‌ها
    skills = SlillTraining.objects.all().order_by('category')

    # دسته‌بندی مهارت‌ها
    skills_in_category = []
    categories = skills.values_list('category', flat=True).distinct()
    for cat in categories:
        items = skills.filter(category=cat)
        skills_in_category.append({"category": cat, "items": items,'counts':len(items)})

    total_categories= len(categories)
    total_items= len(skills)
    return render(request, f"{template_pages}/list.html", {
        'skills': skills,
        'skills_in_category': skills_in_category,
        'categories':categories,
        'total_categories':total_categories,
        'total_items':total_items
    })
def skill_create(request):
    categories = SlillTraining.objects.values_list("category", flat=True).distinct()
   
    # فرم ایجاد مهارت، بعدا اضافه می‌کنیم
    return render(request, f"{template_pages}/create.html",{"categories": categories})

def categories(request):
    # نمایش دسته‌بندی‌ها
    categories = SlillTraining.objects.values_list("category", flat=True).distinct()
    return render(request, f"{template_pages}/categories.html", {"categories": categories})

def skill_detail(request, pk):
    skill = get_object_or_404(SlillTraining, pk=pk)
    return render(request, f"{template_pages}/detail.html", {"skill": skill})


def create_manual(request):
    if request.method == "POST":
        data = request.POST
        titles =  data.get("title[]",[])
        categories =data.get("category[]",[])
        codes = data.get("code[]",[]) 
        values = {
           'titles':titles,
           'titles':categories,
           'codes':codes,
        }
        return redirect("skills:create")

           
    return redirect("skills:create")

# views.py
import uuid
import time
from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib import messages
from django.http import StreamingHttpResponse
import openpyxl
from .models import SlillTraining
from django.db import transaction

from django.http import JsonResponse, StreamingHttpResponse
from django.db import transaction
import uuid
import time
from django.core.cache import cache
import openpyxl
from .models import SlillTraining

def create_excel(request):
    """
    آپلود و ثبت یا بروزرسانی مهارت‌ها از فایل Excel.
    از شناسه یکتا برای هر آپلود استفاده می‌شود تا SSE درست کار کند.
    """
    if request.method == "POST" and request.FILES.get("skills_excel"):
        upload_id = request.POST.get("upload_id")  # از کلاینت بگیر
        if not upload_id:
            return JsonResponse({"error": "upload_id نیاز است"}, status=400)
        excel_file = request.FILES["skills_excel"]
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active
        total_rows = sheet.max_row - 1

        cache.set(f"excel_progress_{upload_id}", 0)

        # استفاده از تراکنش برای جلوگیری از lock طولانی
        with transaction.atomic():
            for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=1):
                category, title, code = row
                SlillTraining.objects.update_or_create(
                    title=title,
                    defaults={'category': category, 'code': code}
                )

                # بروزرسانی درصد پیشرفت
                progress = int((idx / total_rows) * 100)
                cache.set(f"excel_progress_{upload_id}", progress)
                print(f"excel_progress_{upload_id}",progress)
                time.sleep(0.05)  # فقط برای شبیه‌سازی (در تولید حذف شود)

        # تکمیل progress
        cache.set(f"excel_progress_{upload_id}", 100)

        # پاسخ JSON به کلاینت
        return JsonResponse({"success": True, "upload_id": upload_id, "message": "مهارت‌ها با موفقیت ثبت یا بروزرسانی شدند."})

    return JsonResponse({"success": False, "message": "هیچ فایلی ارسال نشده است."}, status=400)


def create_excel_stream(request):
    """
    SSE برای ارسال درصد پیشرفت آپلود به کلاینت.
    باید upload_id از query string دریافت شود.
    """
    upload_id = request.GET.get("upload_id")
    if not upload_id:
        return StreamingHttpResponse("data: 100\n\n", content_type="text/event-stream")

    def event_stream():
        while True:
            progress = cache.get(f"excel_progress_{upload_id}", 0)
            print(f"event_stream_{upload_id}",progress)
            yield f"data: {progress}\n\n"
            if progress >= 100:
                break
            time.sleep(0.5)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

def download_sample_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Skills Sample"

    # هدر
    ws.append([ "دسته‌بندی","عنوان مهارت", "کد مهارت"])

    # مثال نمونه
    ws.append([ "بهداری","مهارت بهداری", "1400045"])
    ws.append(["فنی","مهارت فنی", "1400046"])

    # پاسخ
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=skills_sample.xlsx'
    wb.save(response)
    return response
 

def export_skills_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "اکسل مهارت ها"

    header_font = Font(color="FFFFFF", bold=True)  # متن سفید و بولد
    header_fill = PatternFill(start_color="0288D1", end_color="0288D1", fill_type="solid")  # آبی پر رنگ
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    center_align = Alignment(horizontal="center", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")  # برای RTL

    headers = ["ردیف", "دسته‌بندی", "عنوان مهارت", "کد مهارت", "تعداد سربازان"]
    ws.append(headers)
    for col_num, cell in enumerate(ws[1], 1):
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = center_align

    skills = SlillTraining.objects.all().order_by('category', 'title')

    for idx, skill in enumerate(skills, start=1):
        total_soldiers = skill.primary_soldiers.count() + skill.secondary_soldiers.count()
        row = [
            idx,
            skill.category,
            skill.title,
            skill.code,
            total_soldiers
        ]
        ws.append(row)
        for col_num, cell in enumerate(ws[idx+1], 1):
            cell.border = thin_border
            if col_num == 2 or col_num == 3: 
                cell.alignment = right_align
            else:
                cell.alignment = center_align

    column_widths = [8, 20, 30, 15, 15]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

    ws.sheet_view.rightToLeft = True
    today = jdatetime.date.today()
    date_str = today.strftime("%d-%m-%Y")  
    filename = f"اکسل مهارت ها - {date_str}.xlsx"
    quoted_filename = urllib.parse.quote(filename)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{quoted_filename}"

    wb.save(response)
    return response

from django.core.paginator import Paginator

from django.core.paginator import Paginator
from django.shortcuts import render
from battalions.models import battalion, battalion_group

def assign_view(request):
    # شروع با queryset همه سربازان داوطلب
    all_soldiers = Soldier.objects.filter(willing_to_learn=True).order_by('code_gorhan_nahai')

    # ===== دریافت فیلترها از GET =====
    search = request.GET.get('search', '').strip()
    gordan = request.GET.get('gordan', '').strip()
    battaliongroup = request.GET.get('battaliongroup', '').strip()
    skill_1 = request.GET.get('skill_1', '').strip()
    skill_2 = request.GET.get('skill_2', '').strip()
    code_paziresh = request.GET.get('code_paziresh', '').strip()

    soldiers = all_soldiers

    if search:
        soldiers = soldiers.filter(
            Q(National_Code__icontains=search) |
            Q(name__icontains=search) |
            Q(family__icontains=search)
        )
    if gordan:
        soldiers = soldiers.filter(t_Gordan__name__icontains=gordan)

    if battaliongroup:
        if gordan is not None:
            soldiers = soldiers.filter(t_battalion_group__name__icontains=battaliongroup)

    if skill_1:
        soldiers = soldiers.filter(skill_1__id=skill_1)
    if skill_2:
        soldiers = soldiers.filter(skill_2__id=skill_2)
    if code_paziresh:
        soldiers = soldiers.filter(code_paziresh__icontains=code_paziresh)


    # ===== Pagination =====
    page_number = request.GET.get('page', 1)
    paginator = Paginator(soldiers, 20)
    try:
        soldiers_page = paginator.get_page(page_number)
    except:
        soldiers_page = paginator.get_page(1)

    # ===== لیست مهارت‌ها و دسته‌بندی‌ها =====
    skills = SlillTraining.objects.all().order_by("category", "title")
    categories = SlillTraining.objects.values_list("category", flat=True).distinct()

    # گردان‌ها و گروهان‌ها
    gordans = battalion.objects.all()
    gorohans = battalion_group.objects.all()

     # بررسی تغییر تعداد (مثل op_result)
    op_result = soldiers.count() != all_soldiers.count()

    context = {
        'soldiers': soldiers_page,
        'skills': skills,
        'categories': categories,
        'total_soldiers': soldiers.count(),
        'total_skills': skills.count(),
        'gordans': gordans,
        'gorohans': gorohans,
        'request': request,  # برای حفظ مقادیر فرم
        'op_result': op_result,
    }
    return render(request,  f"{template_pages}/assign.html", context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required


@login_required
@transaction.atomic
def assign_create_manual(request):
    if request.method == "POST":
        # استخراج ID سربازها از کلیدهای فرم
        soldier_ids = set()
        for key in request.POST.keys():
            if key.startswith("skill_1_") or key.startswith("skill_2_"):
                try:
                    soldier_id = int(key.split("_")[-1])
                    soldier_ids.add(soldier_id)
                except ValueError:
                    continue

        # گرفتن فقط سربازانی که در فرم آمده‌اند
        soldiers = Soldier.objects.filter(id__in=soldier_ids)

        def get_or_create_skill(title):
            if not title:
                return None
            skill, _ = SlillTraining.objects.get_or_create(
                title=title,
                defaults={"category": "", "code": ""}
            )
            return skill

        # ثبت مهارت‌ها برای هر سرباز
        for soldier in soldiers:
            skill_1_value = request.POST.get(f"skill_1_{soldier.id}", "").strip()
            skill_2_value = request.POST.get(f"skill_2_{soldier.id}", "").strip()

            soldier.skill_1 = get_or_create_skill(skill_1_value)
            soldier.skill_2 = get_or_create_skill(skill_2_value)
            soldier.save()

        messages.success(request, "مهارت‌ها با موفقیت ثبت شدند.")

        # 🟢 برگشت به همان صفحه (با query string)
        next_url = request.META.get("HTTP_REFERER", None)
        if next_url:
            return redirect(next_url)
        return redirect("skills:assign")

    # در حالت GET
    return redirect("skills:assign")

def assign_soldier_slills_manual():
   return redirect("skills:assign")


import openpyxl
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment
from django.http import HttpResponse

def assign_soldier_skills_excel(request, mode):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "مهارت سربازان"

    # انتخاب نوع خروجی
    if mode == "full":
        headers = ["ردیف", "کدملی", "نام", "نام خانوادگی", "نام پدر", "مهارت اول", "کد مهارت اول", "مهارت دوم", "کد مهارت دوم"]
        queryset = Soldier.objects.filter(skill_1__isnull=False) | Soldier.objects.filter(skill_2__isnull=False)
    elif mode == "codes":
        headers = ["ردیف", "کدملی", "نام", "نام خانوادگی", "نام پدر", "کد مهارت اول", "کد مهارت دوم"]
        queryset = Soldier.objects.filter(skill_1__isnull=False) | Soldier.objects.filter(skill_2__isnull=False)
    elif mode == "titles":
        headers = ["ردیف", "کدملی", "نام", "نام خانوادگی", "نام پدر", "مهارت اول", "مهارت دوم"]
        queryset = Soldier.objects.filter(skill_1__isnull=False) | Soldier.objects.filter(skill_2__isnull=False)
    elif mode == "all":
        headers = ["ردیف", "کدملی", "نام", "نام خانوادگی", "نام پدر", "مهارت اول", "کد مهارت اول", "مهارت دوم", "کد مهارت دوم"]
        queryset = Soldier.objects.all()
    else:
        return redirect("skills:assign")

    # استایل هدر
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")  # آبی آسمانی تیره
    header_font = Font(color="FFFFFF", bold=True)  # سفید
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    # نوشتن هدر
    ws.append(headers)
    for col_num, _ in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # نوشتن داده‌ها
    for i, soldier in enumerate(queryset, start=1):
        if mode == "full":
            row = [
                i, soldier.National_Code, soldier.name, soldier.family, soldier.fathers_name,
                soldier.skill_1.title if soldier.skill_1 else "",
                soldier.skill_1.code if soldier.skill_1 else "",
                soldier.skill_2.title if soldier.skill_2 else "",
                soldier.skill_2.code if soldier.skill_2 else "",
            ]
        elif mode == "codes":
            row = [
                i, soldier.National_Code, soldier.name, soldier.family, soldier.fathers_name,
                soldier.skill_1.code if soldier.skill_1 else "",
                soldier.skill_2.code if soldier.skill_2 else "",
            ]
        elif mode == "titles":
            row = [
                i, soldier.National_Code, soldier.name, soldier.family, soldier.fathers_name,
                soldier.skill_1.title if soldier.skill_1 else "",
                soldier.skill_2.title if soldier.skill_2 else "",
            ]
        elif mode == "all":
            row = [
                i, soldier.National_Code, soldier.name, soldier.family, soldier.fathers_name,
                soldier.skill_1.title if soldier.skill_1 else "",
                soldier.skill_1.code if soldier.skill_1 else "",
                soldier.skill_2.title if soldier.skill_2 else "",
                soldier.skill_2.code if soldier.skill_2 else "",
            ]
        ws.append(row)

        # استایل برای هر سطر داده
        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=i + 1, column=col_num)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center")

    # تنظیم عرض ستون‌ها
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[col_letter].width = max_length + 2
    ws.sheet_view.rightToLeft = True

    # خروجی HTTP
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="soldiers_skills_{mode}.xlsx"'
    wb.save(response)
    return response


def skills_actions_(request):
    if request.method == "POST":
        action = request.POST.get("action")
        ids = request.POST.getlist("selected")

        # 🟢 حذف موارد انتخاب شده
        if action == "delete":
            if not ids:
                messages.warning(request, "هیچ مهارتی برای حذف انتخاب نشده است.")
            else:
                deleted_count, _ = SlillTraining.objects.filter(id__in=ids).delete()
                if deleted_count:
                    messages.success(request, f"{deleted_count} مهارت با موفقیت حذف شد.")
                else:
                    messages.error(request, "عملیات حذف موفقیت‌آمیز نبود!")

        # 🟡 بروزرسانی دسته
        elif action == "edit_category":
            new_category = request.POST.get("new_category")
            if not ids:
                messages.warning(request, "هیچ مهارتی انتخاب نشده است تا دسته آن تغییر کند.")
            elif not new_category:
                messages.warning(request, "لطفاً نام دسته جدید را وارد کنید.")
            else:
                updated_count = SlillTraining.objects.filter(id__in=ids).update(category=new_category)
                if updated_count:
                    messages.success(request, f"دسته {updated_count} مهارت به '{new_category}' تغییر یافت.")
                else:
                    messages.error(request, "عملیات بروزرسانی دسته موفقیت‌آمیز نبود!")

        # 🟠 بروزرسانی کد
        elif action == "edit_code":
            new_code = request.POST.get("new_code")
            if not ids:
                messages.warning(request, "هیچ مهارتی انتخاب نشده است تا کد آن تغییر کند.")
            elif not new_code:
                messages.warning(request, "لطفاً مقدار کد جدید را وارد کنید.")
            else:
                updated_count = SlillTraining.objects.filter(id__in=ids).update(code=new_code)
                if updated_count:
                    messages.success(request, f"کد {updated_count} مهارت به '{new_code}' تغییر یافت.")
                else:
                    messages.error(request, "عملیات بروزرسانی کد موفقیت‌آمیز نبود!")

        # 🔵 اعمال تغییرات input ها
        elif action == "apply_changes":
            changes = {}
            for key, value in request.POST.items():
               if key.startswith("field_changed_"):
                     _,_c, pk, field = key.split("_")
                     if pk not in changes:
                        changes[pk] = {}
                     changes[pk][field] = value
            if not changes:
                messages.warning(request, "هیچ تغییری برای اعمال وجود ندارد.")
            else:
                for pk, fields in changes.items():
                    obj = get_object_or_404(SlillTraining, pk=pk)
                    for f, v in fields.items():
                        setattr(obj, f, v)
                    obj.save()
                messages.success(request, f"{len(changes)} مورد با موفقیت بروزرسانی شد.")
            

        # ⚠️ هیچ عملیاتی انتخاب نشده
        else:
            messages.warning(request, "هیچ عملیاتی انتخاب نشده است.")

    return redirect("skills:list")


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import SlillTraining  # نام مدل طبق پروژه شما
from django.db import transaction

def skills_actions(request):
    """اعمال تمام تغییرات مهارت‌ها (حذف، ویرایش، افزودن) در یک مرحله"""
    if request.method != "POST":
        return redirect("skills:list")

    action = request.POST.get("action")
    if action != "apply_changes":
        messages.warning(request, "فقط از طریق دکمه «اعمال تغییرات» می‌توانید تغییرات را ثبت کنید.")
        return redirect("skills:list")

    # همه تغییرات را از فرم بگیر
    changes = {}
    added = []
    deleted = request.POST.getlist("deleted_ids", [])
    fields = request.POST.items()
    # 🟢 بررسی فیلدهای تغییر یافته
    for key, value in fields:
        if key.startswith("changed_"):
            # مثال: field_changed_12_title
            _, pk, field = key.split("_", 2)
            if pk not in changes:
                changes[pk] = {}
            changes[pk][field] = value

        elif key.startswith("new_"):  # مثال: new_1_title
            parts = key.split("_")
            if len(parts) >= 3:
                new_id = parts[1]
                field = parts[2]
                while len(added) < int(new_id):
                    added.append({})
                added[int(new_id) - 1][field] = value

    total_updated = 0
    total_added = 0
    total_deleted = 0

    try:
        with transaction.atomic():
            # 🟠 حذف رکوردها
            if deleted:
                total_deleted, _ = SlillTraining.objects.filter(id__in=deleted).delete()

            # 🔵 بروزرسانی رکوردها
            for pk, fields in changes.items():
                obj = get_object_or_404(SlillTraining, pk=pk)
                for field, value in fields.items():
                    setattr(obj, field, value)
                obj.save()
                total_updated += 1

            # 🟢 افزودن رکوردهای جدید
            for item in added:
                if any(item.values()):
                    SlillTraining.objects.create(
                        category=item.get("category", ""),
                        title=item.get("title", ""),
                        code=item.get("code", "")
                    )
                    total_added += 1

    except Exception as e:
        messages.error(request, f"خطا در ذخیره تغییرات: {e}")
        return redirect("skills:list")

    # ✅ نمایش پیام نتیجه
    msg_parts = []
    if total_updated: msg_parts.append(f"{total_updated} مورد ویرایش شد")
    if total_added: msg_parts.append(f"{total_added} مهارت جدید افزوده شد")
    if total_deleted: msg_parts.append(f"{total_deleted} مورد حذف شد")
    if not msg_parts:
        msg_parts.append("هیچ تغییری اعمال نشد")

    messages.success(request, "، ".join(msg_parts))
    return redirect("skills:list")

import jdatetime
from .forms import HazardSettingsForm
from .models import HazardSettings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

class CreateOrUpdateHazardSettings(LoginRequiredMixin, View):
    def get(self, request):
        hz = HazardSettings.objects.last()
        form = HazardSettingsForm()

        persian_months = [
            "فروردین", "اردیبهشت", "خرداد", "تیر",
            "مرداد", "شهریور", "مهر", "آبان",
            "آذر", "دی", "بهمن", "اسفند"
        ]

        if hz is not None:
            # تبدیل تاریخ‌های میلادی به شمسی
            certificate_date_sh = jdatetime.date.fromgregorian(date=hz.certificate_date).strftime("%Y/%m/%d")
            start_date_sh = jdatetime.date.fromgregorian(date=hz.start_date).strftime("%Y/%m/%d")
            end_date_sh = jdatetime.date.fromgregorian(date=hz.end_date).strftime("%Y/%m/%d")

            form.initial.update({
                'certificate_date': certificate_date_sh,
                'letter_number': hz.letter_number,
                'year': hz.year,
                'month_name': hz.month_name,
                'first_aid_hours': hz.first_aid_hours,
                'hazard_preparedness_hours': hz.hazard_preparedness_hours,
                'start_date': start_date_sh,
                'end_date': end_date_sh,
            })
        else:
            # تاریخ شمسی امروز
            now = jdatetime.date.today()
            start_of_month = jdatetime.date(now.year, now.month, 1)
            end_of_period = start_of_month + jdatetime.timedelta(days=4)

            form.initial.update({
                'certificate_date': now.strftime("%Y/%m/%d"),
                'year': now.year,
                'month_name': persian_months[now.month - 1],
                'first_aid_hours': 22,
                'hazard_preparedness_hours': 8,
                'start_date': start_of_month.strftime("%Y/%m/%d"),
                'end_date': end_of_period.strftime("%Y/%m/%d"),
            })

        context = {'form': form, 'hazard': hz}
        return render(request, f"{template_pages}/certificate_hazard.html", context)

    def post(self, request):
        hz = HazardSettings.objects.last()
        form = HazardSettingsForm(request.POST or None)

        if not form.is_valid():
            return render(request, f"{template_pages}/certificate_hazard.html", {'form': form, 'hazard': hz})

        # دریافت داده‌ها و ذخیره در مدل
        data = form.cleaned_data
        if hz is None:
            hz = HazardSettings()

        for key, value in data.items():
            setattr(hz, key, value)
        hz.save()

        return redirect('skills:certificates_hazard')

from ensaniapp_settings.models import EnsaniSettings
import jdatetime
from django.shortcuts import render

def certificates_hazard_print(request):
    # دریافت پارامتر مرتب‌سازی از query string
    order_by = request.GET.get('order_by', 'acceptance_code')

    # تنظیم فیلدهای مرتب‌سازی بر اساس نوع انتخاب
    if order_by == 'structure':
        order_fields = ['t_Gordan__name', 't_battalion_group__name','code_gorhan_nahai']
    else:
        order_fields = ['acceptance_code']

    # واکشی سربازان با ترتیب مشخص
    soldiers = (
        Soldier.objects
        .filter(in_coures=True, willing_to_learn=True)
        .order_by(*order_fields)
    )

    hazard = HazardSettings.objects.first()
    ens = EnsaniSettings.objects.all()

    # تبدیل تاریخ‌های Hazard به شمسی
    def to_shamsi(date_obj):
        if date_obj:
            return jdatetime.date.fromgregorian(date=date_obj).strftime("%Y/%m/%d")
        return "-"

    hazard_shamsi = None
    if hazard:
        hazard_shamsi = {
            "certificate_date": to_shamsi(hazard.certificate_date),
            "letter_number": hazard.letter_number,
            "year": hazard.year,
            "month_name": hazard.month_name,
            "first_aid_hours": hazard.first_aid_hours,
            "hazard_preparedness_hours": hazard.hazard_preparedness_hours,
            "start_date": to_shamsi(hazard.start_date),
            "end_date": to_shamsi(hazard.end_date),
        }

    context = {
        'hazard': hazard_shamsi,
        'ens': ens,
        'soldiers': soldiers,
        'order_by':order_by,
    }
    return render(request, f"{template_pages}/certificates_hazard_print.html", context)
