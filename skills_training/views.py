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
from accounts.decorators import permissions_required

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
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.shortcuts import render
from battalions.models import battalion, battalion_group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

import openpyxl
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment
from django.http import HttpResponse

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import SlillTraining  # نام مدل طبق پروژه شما
from django.db import transaction
import jdatetime
from .forms import HazardSettingsForm
from .models import HazardSettings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

template_pages = 'pages'

@login_required
# @permissions_required(
#     main_permission='dep.niru_ensani',
#     fallback_permission='dep.gorohan',
#     fallback_url='skills:assign',
#     redirect_url='account_access_403'
# )
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


from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from soldiers.models import Soldier, SlillTraining
from ensani_soldires_management.access import get_user_battalion_groups,get_user_battalions,get_user_soldiers

def assign_view(request):
    """
    نمایش سربازان با امکان فیلتر بر اساس جستجو، گردان، گروهان، مهارت و کد پذیرش.
    نمایش تنها سربازانی که کاربر به آن‌ها دسترسی دارد.
    """
    # ===== سربازان با دسترسی کاربر =====
    all_soldiers = get_user_soldiers(request.user).filter(willing_to_learn=True).order_by('code_gorhan_nahai')

    # ===== دریافت فیلترها از GET =====
    search = request.GET.get('search', '').strip()
    gordan = request.GET.get('gordan', '').strip()
    battaliongroup = request.GET.get('battaliongroup', '').strip()
    skill_1 = request.GET.get('skill_1', '').strip()
    skill_2 = request.GET.get('skill_2', '').strip()
    code_paziresh = request.GET.get('code_paziresh', '').strip()

    soldiers = all_soldiers

    # ===== فیلتر جستجو =====
    if search:
        soldiers = soldiers.filter(
            Q(National_Code__icontains=search) |
            Q(name__icontains=search) |
            Q(family__icontains=search)
        )

    # ===== فیلتر گردان بر اساس ID =====
    if gordan:
        try:
            gordan_id = int(gordan)
            soldiers = soldiers.filter(t_Gordan__id=gordan_id)
        except ValueError:
            pass

    # ===== فیلتر گروهان بر اساس ID =====
    if battaliongroup:
        try:
            battaliongroup_id = int(battaliongroup)
            soldiers = soldiers.filter(t_battalion_group__id=battaliongroup_id)
        except ValueError:
            pass

    # ===== فیلتر مهارت‌ها =====
    if skill_1:
        soldiers = soldiers.filter(skill_1__id=skill_1)
    if skill_2:
        soldiers = soldiers.filter(skill_2__id=skill_2)

    # ===== فیلتر کد پذیرش =====
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

    # ===== گردان‌ها و گروهان‌ها با توجه به دسترسی کاربر =====
    gordans = get_user_battalions(request.user)
    gorohans = get_user_battalion_groups(request.user)

    # ===== بررسی تغییر تعداد برای op_result =====
    op_result = soldiers.count() != all_soldiers.count()
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()

    # ===== Context =====
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
        'query_params': query_string
    }
    return render(request, f"{template_pages}/assign.html", context)

from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
@transaction.atomic
def assign_create_manual(request):
    if request.method != "POST":
        return redirect("skills:assign")

    # ===============================
    # 1️⃣ استخراج ID سربازها
    # ===============================
    soldier_ids = {
        int(key.split("_")[-1])
        for key in request.POST.keys()
        if key.startswith(("skill_1_", "skill_2_")) and key.split("_")[-1].isdigit()
    }

    if not soldier_ids:
        messages.warning(request, "سربازی انتخاب نشده است.")
        return redirect(request.META.get("HTTP_REFERER", "skills:assign"))

    # ===============================
    # 2️⃣ قفل سربازها (Row-level Lock)
    # ===============================
    soldiers = list(
        Soldier.objects
        .select_for_update()
        .filter(id__in=soldier_ids)
    )

    # ===============================
    # 3️⃣ جمع‌آوری مهارت‌ها (unique)
    # ===============================
    skill_titles = set()

    for soldier in soldiers:
        s1 = request.POST.get(f"skill_1_{soldier.id}", "").strip()
        s2 = request.POST.get(f"skill_2_{soldier.id}", "").strip()
        if s1:
            skill_titles.add(s1)
        if s2:
            skill_titles.add(s2)

    # ===============================
    # 4️⃣ گرفتن مهارت‌های موجود
    # ===============================
    existing_skills = {
        s.title: s
        for s in SlillTraining.objects.filter(title__in=skill_titles)
    }

    # ===============================
    # 5️⃣ ساخت مهارت‌های جدید (bulk_create)
    # ===============================
    new_skills = [
        SlillTraining(title=title, category="", code="")
        for title in skill_titles
        if title not in existing_skills
    ]

    if new_skills:
        SlillTraining.objects.bulk_create(new_skills)
        # دوباره واکشی
        for s in SlillTraining.objects.filter(title__in=skill_titles):
            existing_skills[s.title] = s

    # ===============================
    # 6️⃣ ست کردن skill ها روی سربازها
    # ===============================
    for soldier in soldiers:
        s1 = request.POST.get(f"skill_1_{soldier.id}", "").strip()
        s2 = request.POST.get(f"skill_2_{soldier.id}", "").strip()

        soldier.skill_1 = existing_skills.get(s1)
        soldier.skill_2 = existing_skills.get(s2)

    # ===============================
    # 7️⃣ ذخیره گروهی
    # ===============================
    Soldier.objects.bulk_update(soldiers, ['skill_1', 'skill_2'])

    messages.success(request, "مهارت‌ها با موفقیت ثبت شدند.")

    return redirect(request.META.get("HTTP_REFERER", "skills:assign"))

def assign_soldier_slills_manual():
   return redirect("skills:assign")


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
        form.clean()
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


from .models import TechnicalVocational


from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

def technical_vocational_page(request):
    technical_vocationals = (
        TechnicalVocational.objects
        .annotate(soldier_count=Count('soldier'))
        .order_by('-code')
    )
    selected_field = None
    all_soldiers = Soldier.objects.all()
    soldiers = []


    # 📌 فیلتر رشته انتخاب‌شده از query string یا فرم
    field_id = request.GET.get("technical_vocational_id") or request.POST.get("technical_vocational_id")
    if field_id:
        try:
            selected_field = TechnicalVocational.objects.get(id=field_id)
            soldiers = all_soldiers.filter(technical_exam=selected_field)
        except TechnicalVocational.DoesNotExist:
            messages.error(request, "رشته انتخاب شده معتبر نیست.")
            selected_field = None
    else:
        # اگر رشته انتخاب نشده بود، همه سربازهایی که آزمون دارند رو نشون بده
        soldiers = all_soldiers.filter(technical_exam__isnull=False)
    
    soldiers = soldiers.order_by('-technical_exam_submit_datetime')

    # 📄 Pagination: هر صفحه حداکثر 20 سرباز
    paginator = Paginator(soldiers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    counts_in_selected_field = all_soldiers.filter(technical_exam=selected_field).count()
    counts_in_all = all_soldiers.filter(technical_exam__isnull=False).count()
    context = {
        'counts_in_selected_field':counts_in_selected_field,
        'counts_in_all':counts_in_all,
        "technical_vocationals": technical_vocationals,
        "selected_field": selected_field,
        "soldiers": page_obj,  # سربازها به‌صورت صفحه‌بندی شده
        "all_soldiers": all_soldiers,
        "page_obj": page_obj,  # برای کنترل در template
    }
    return render(request, f"{template_pages}/technical_vocational.html", context)

# ==================== ایجاد ====================
def technical_vocational_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        if not name or not code:
            messages.error(request, "نام و کد رشته باید وارد شود.")
        else:
            # بررسی یکتا بودن name و code
            if TechnicalVocational.objects.filter(name=name).exists():
                messages.error(request, "این نام رشته قبلاً ثبت شده است.")
            elif TechnicalVocational.objects.filter(code=code).exists():
                messages.error(request, "این کد رشته قبلاً ثبت شده است.")
            else:
                TechnicalVocational.objects.create(name=name, code=code)
                messages.success(request, "رشته ایجاد شد.")
    return redirect("skills:technical_vocational")

# ==================== بروزرسانی ====================
def technical_vocational_update(request, pk):
    field = get_object_or_404(TechnicalVocational, id=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        # بررسی یکتا بودن قبل از بروزرسانی
        if name and TechnicalVocational.objects.exclude(id=pk).filter(name=name).exists():
            messages.error(request, "این نام رشته قبلاً ثبت شده است.")
        elif code and TechnicalVocational.objects.exclude(id=pk).filter(code=code).exists():
            messages.error(request, "این کد رشته قبلاً ثبت شده است.")
        else:
            if name: field.name = name
            if code: field.code = code
            field.save()
            messages.success(request, "رشته بروزرسانی شد.")
    return redirect("skills:technical_vocational")

# ==================== حذف ====================
def technical_vocational_delete(request, pk):
    field = get_object_or_404(TechnicalVocational, id=pk)
    if request.method == "POST":
        field.delete()
        messages.success(request, "رشته حذف شد.")
    return redirect("skills:technical_vocational")

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def technical_vocational_add_soldier(request): 
    if request.method != "POST":
        messages.error(request, "درخواست معتبر نیست.")
        return redirect(request.META.get("HTTP_REFERER", "skills:technical_vocational"))

    # گرفتن داده‌ها از فرم
    field_id = request.POST.get("technical_vocational_id")
    soldier_id = request.POST.get("soldire_id")

    if not field_id or not soldier_id:
        messages.error(request, "لطفاً سرباز و رشته را انتخاب کنید.")
        return redirect(request.META.get("HTTP_REFERER", "skills:technical_vocational"))

    # دریافت رشته و سرباز
    field = get_object_or_404(TechnicalVocational, id=field_id)
    soldier = get_object_or_404(Soldier, id=soldier_id)

    # بررسی اینکه سرباز قبلاً به این رشته اختصاص داده نشده باشد
    if soldier.technical_exam == field:
        messages.warning(request, f"سرباز {soldier} قبلاً به رشته {field.name} اختصاص داده شده است.")
        return redirect(request.META.get("HTTP_REFERER", "skills:technical_vocational"))

    # اختصاص سرباز به رشته
    soldier.technical_exam = field
    soldier.technical_exam_submit_datetime = timezone.now()

    uploaded_file = request.FILES.get('avatar')
    if uploaded_file:
        soldier.save_avatar(uploaded_file)

    soldier.save()

    messages.success(request, f"سرباز {soldier} با موفقیت به رشته {field.name} اضافه شد.")
    return redirect(request.META.get("HTTP_REFERER", "skills:technical_vocational"))

def technical_vocational_eazy_register(request):
    # می‌تونی اطلاعات لازم مثل رشته‌ها یا سربازان را اینجا پاس بدهی
    technical_vocationals = TechnicalVocational.objects.all().order_by('-code')
    soldiers = Soldier.objects.filter(technical_exam__isnull=False).order_by('name')
    last_registered_soldiers = soldiers.order_by('-technical_exam_submit_datetime')[:19]
        # 📌 فیلتر رشته انتخاب‌شده از query string یا فرم
    field_id = request.GET.get("technical_vocational_id") or request.POST.get("technical_vocational_id")

    selected_field=None
    if field_id:
        try:
            selected_field = TechnicalVocational.objects.get(id=field_id)
            if not selected_field:
                selected_field = TechnicalVocational.objects.first()
        except TechnicalVocational.DoesNotExist:
            pass
 
    if request.method == "POST":
        soldier_id = request.POST.get("soldire_id")
        technical_vocational_id = request.POST.get("technical_vocational_id")
        avatar_data = request.POST.get("avatar")  # base64 image
        
        # ثبت اطلاعات سرباز
        if soldier_id and technical_vocational_id:
            try:
                soldier = Soldier.objects.get(id=soldier_id)
                technical_field = TechnicalVocational.objects.get(id=technical_vocational_id)
                
                soldier.technical_exam = technical_field
                soldier.technical_exam_submit_datetime = timezone.now()
                
                # ذخیره عکس در صورت آپلود
                uploaded_file = request.FILES.get('file')
                
                if uploaded_file:
                    soldier.save_avatar(uploaded_file)

                soldier.save()
                
                # ریدایرکت بعد از ثبت
                return redirect(request.path + f"?technical_vocational_id={technical_vocational_id}")
            except (Soldier.DoesNotExist, TechnicalVocational.DoesNotExist):
                pass  # می‌توان پیام خطا نمایش داد

    context = {
        "selected_field":selected_field,
        "technical_vocationals": technical_vocationals,
        "soldiers": soldiers,
        'last_registered_soldiers':last_registered_soldiers
    }
    return render(request, f"{template_pages}/technical_vocational_eazy_register.html", context)

import os
import zipfile
import tempfile
from django.http import HttpResponse
from openpyxl import Workbook
from ensaniapp_settings.models import EnsaniSettings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from io import BytesIO

def technical_vocational_soldiers_export():
    soldiers = Soldier.objects.filter(technical_exam__isnull=False).order_by('name')
    wb = Workbook()
    ws = wb.active
    ws.title = "سربازان فنی و حرفه‌ای"

    headers = ["ردیف", "نام", "نام خانوادگی", "کد ملی", "رشته", "کد رشته","تصویر"]
    ws.append(headers)

    # استایل هدر
    header_font = Font(bold=True, color="000000")
    header_fill = PatternFill(start_color="92DCE5", end_color="92DCE5", fill_type="solid")
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # داده‌ها
    for i, soldier in enumerate(soldiers, 2):
        values = [
            i-1,
            soldier.name,
            soldier.family,
            soldier.National_Code,
            soldier.technical_exam.name if soldier.technical_exam else "",
            soldier.technical_exam.code if soldier.technical_exam else "",
            "دارد" if soldier.avatar else "ندارد",
        ]
        for col_num, value in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_num, value=value)
            cell.font = Font(color="000000")
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center', vertical='center')

    # تنظیم عرض ستون‌ها
    for col in ws.columns:
        max_length = max(len(str(c.value)) if c.value else 0 for c in col) + 2
        ws.column_dimensions[col[0].column_letter].width = max_length
    
    ws.sheet_view.rightToLeft = True

    return wb

def technical_vocational_soldiers_export_excel(request):
    wb = technical_vocational_soldiers_export()
    ensani_settings = EnsaniSettings.objects.first()
    course_number = ensani_settings.shomare_dore if ensani_settings else "default"

    # آماده‌سازی پاسخ HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=fani_herfeii_sodliers.xlsx'
    wb.save(response)
    return response

def technical_vocational_soldiers_export_zip(request):
    soldiers = Soldier.objects.filter(technical_exam__isnull=False).order_by('name')
    wb = technical_vocational_soldiers_export()
    ensani_settings = EnsaniSettings.objects.first()
    course_number = ensani_settings.shomare_dore if ensani_settings else "default"

    # ساخت ZIP در حافظه
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # ذخیره اکسل در ZIP
        excel_buffer = BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        zipf.writestr("fani_herfeii_soldiers.xlsx", excel_buffer.read())

        # اضافه کردن تصاویر سربازان
        for soldier in soldiers:
            if soldier.avatar:
                try:
                    with default_storage.open(soldier.avatar.name, 'rb') as f:
                        data = f.read()
                        filename = f"pictures/{soldier.National_Code}.png"
                        zipf.writestr(filename, data)
                except Exception as e:
                    print(f"خطا در افزودن تصویر {soldier.National_Code}: {e}")

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=fani_herfeii.zip'
    return response