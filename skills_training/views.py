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

template_pages = 'pages'

def index(request):
    # تعداد کل مهارت‌ها
    total_skills = SlillTraining.objects.count()

    # تعداد دسته‌های منحصر به فرد
    total_categories = SlillTraining.objects.values('category').distinct().count()

    # تعداد مهارت‌هایی که کد ندارند
    skills_without_code = SlillTraining.objects.filter(Q(code__isnull=True) | Q(code__exact='')).count()

    # تعداد سربازان با حداقل یک مهارت
    soldiers_with_skills = Soldier.objects.filter(Q(skill_1__isnull=False) | Q(skill_2__isnull=False)).count()

    # 5 مهارت پر استفاده (براساس تعداد سربازانی که دارند)
    # ابتدا annotate تعداد سربازان برای هر مهارت
    skills_usage = SlillTraining.objects.annotate(
        usage_count=Count('primary_soldiers') + Count('secondary_soldiers')
    ).order_by('-usage_count')[:5]

        # فهرست دسته‌ها: category, skill_counts, soldiers_count
    categories_info = []
    categories = SlillTraining.objects.values_list('category', flat=True).distinct()
    for cat in categories:
        skills_in_cat = SlillTraining.objects.filter(category=cat)
        skill_count = skills_in_cat.count()
        # تعداد سربازانی که حداقل یکی از مهارت‌های این دسته را دارند
        soldiers_count = Soldier.objects.filter(
            Q(skill_1__in=skills_in_cat) | Q(skill_2__in=skills_in_cat)
        ).distinct().count()
        categories_info.append({
            "category": cat,
            "skill_count": skill_count,
            "soldiers_count": soldiers_count
        })
    return render(request, f"{template_pages}/index.html", {
        "total_skills": total_skills,
        "total_categories": total_categories,
        "skills_without_code": skills_without_code,
        "soldiers_with_skills": soldiers_with_skills,
        "top_skills": skills_usage,
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
    if request.method == "POST" and request.FILES.get("skills_excel"):
        excel_file = request.FILES["skills_excel"]
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            category, title, code = row

            # اگر عنوان موجود بود، بروزرسانی کن، در غیر این صورت ایجاد شود
            SlillTraining.objects.update_or_create(
                title=title,
                defaults={
                    'category': category,
                    'code': code
                }
            )

        messages.success(request, "مهارت‌ها از فایل Excel ثبت یا بروزرسانی شدند.")

    return redirect("skills:list")


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
        soldiers = Soldier.objects.filter(willing_to_learn=True)

        for soldier in soldiers:
            # گرفتن مقدار مهارت اول و دوم از فرم
            skill_1_value = request.POST.get(f"skill_1_{soldier.id}")
            skill_2_value = request.POST.get(f"skill_2_{soldier.id}")

            # تابع برای گرفتن یا ساختن مهارت
            def get_or_create_skill(title):
                if not title:
                    return None
                skill = SlillTraining.objects.filter(title=title).first()
                if not skill:
                    skill = SlillTraining.objects.create(
                        title=title,
                        category="",
                        code=""
                    )
                return skill

            # چک کردن و ذخیره برای مهارت ۱
            soldier.skill_1 = get_or_create_skill(skill_1_value)

            # چک کردن و ذخیره برای مهارت ۲
            soldier.skill_2 = get_or_create_skill(skill_2_value)
            # ذخیره تغییرات سرباز
            soldier.save()

        messages.success(request, "مهارت‌ها با موفقیت ثبت شدند.")
    return redirect("skills:assign")  # آدرس صفحه لیست اصلی

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

