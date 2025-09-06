import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from io import BytesIO
from soldiers.models import Soldier
from ensani_letter.models import NormalLetterModels,CheckoutLetterModels


def export_soldiers_to_excel(filter_kwargs=None, filename='export', sheet_name='سربازان', include_stats=True):
    if filter_kwargs is None:
        filter_kwargs = {}

    # ----------------------
    # شیت اصلی: لیست سربازان
    # ----------------------
    queryset = Soldier.objects.filter(**filter_kwargs).values(
        'acceptance_code', 'name', 'family', 'National_Code',
        'Relative_to_inclusive_number', 'phone_number',
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai',
        'Amriye', 'Amriye_organization', 'Sufficiency_of_mobilization',
        'unit_name', 'unit_type', 'has_been_accepted', 'willing_to_learn'
    ).order_by('acceptance_code')

    df = pd.DataFrame(list(queryset))
    df.rename(columns={
        'acceptance_code': 'کد پذیرش',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'National_Code': 'کدملی',
        'Relative_to_inclusive_number': 'شماره والد',
        'phone_number': 'شماره تماس',
        't_Gordan__name': 'نام گردان',
        't_battalion_group__name': 'نام گروهان',
        'code_gorhan_nahai': 'کد گروهان',
        'Amriye': 'وضعیت امریه',
        'Amriye_organization': 'سازمان امریه',
        'Sufficiency_of_mobilization': 'کفایتی',
        'unit_name': 'نام یگان',
        'unit_type': 'نوع یگان',
        'has_been_accepted': 'پذیرش شده',
        'willing_to_learn': 'حاضر به آموزش'
    }, inplace=True)

    bool_columns = ['وضعیت امریه', 'کفایتی', 'پذیرش شده', 'حاضر به آموزش']
    for col in bool_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: 'بلی' if x else 'خیر')

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        ws = writer.sheets[sheet_name]

        # استایل‌ها
        thin_border = Border(
            left=Side(style='thin', color='000000'),
            right=Side(style='thin', color='000000'),
            top=Side(style='thin', color='000000'),
            bottom=Side(style='thin', color='000000')
        )
        header_fill = PatternFill(start_color='87CEEB', end_color='87CEEB', fill_type='solid')
        header_font = Font(name='Vazirmatn', bold=True, color='000000', size=14)
        content_font = Font(name='Vazirmatn', size=11)

        for col_idx, column in enumerate(df.columns, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = thin_border

        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.alignment = Alignment(horizontal='right', vertical='center')
                cell.font = content_font
                cell.border = thin_border

        ws.sheet_view.rightToLeft = True

        for i, col in enumerate(df.columns, 1):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            ws.column_dimensions[get_column_letter(i)].width = max_length

        # ----------------------
        # شیت دوم: آمار از داده شیت اصلی
        # ----------------------
        if include_stats:
            ws2 = writer.book.create_sheet(title='آمار')

            # محاسبه آمار بر اساس df
            total = len(df)
            hadir = df[df['حاضر به آموزش']=='بلی'].shape[0]
            shoro = df[(df['پذیرش شده']=='بلی') & (df['حاضر به آموزش']=='بلی')].shape[0]
            paziresh = df[df['پذیرش شده']=='بلی'].shape[0]
            tatbigh_nashode = df[df['کفایتی']=='خیر'].shape[0]
            yegan_hadir = df[(df['حاضر به آموزش']=='بلی') & (df['پذیرش شده']=='بلی')].shape[0]

            stats = {
                "کل سربازان": total,
                "حاضر به آموزش": hadir,
                "شروع دوره": shoro,
                "کل پذیرش شده‌ها": paziresh,
                "تطبیق نشده": tatbigh_nashode,
                "یگان حاضر": yegan_hadir,
            }

            ws2.append(['عنوان', 'تعداد'])
            for cell in ws2[1]:
                cell.fill = header_fill
                cell.font = Font(name='Vazirmatn', bold=True, size=14)
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = thin_border

            row_fill1 = PatternFill(start_color='E0FFFF', end_color='E0FFFF', fill_type='solid')
            row_fill2 = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')

            for row_num, (key, value) in enumerate(stats.items(), 2):
                fill = row_fill1 if row_num % 2 == 0 else row_fill2
                ws2.cell(row=row_num, column=1, value=key).fill = fill
                ws2.cell(row=row_num, column=1).font = Font(name='Vazirmatn', size=12)
                ws2.cell(row=row_num, column=1).alignment = Alignment(horizontal='right', vertical='center')
                ws2.cell(row=row_num, column=1).border = thin_border

                ws2.cell(row=row_num, column=2, value=value).fill = fill
                ws2.cell(row=row_num, column=2).font = Font(name='Vazirmatn', size=12)
                ws2.cell(row=row_num, column=2).alignment = Alignment(horizontal='center', vertical='center')
                ws2.cell(row=row_num, column=2).border = thin_border

            ws2.sheet_view.rightToLeft = True
            ws2.column_dimensions['A'].width = 25
            ws2.column_dimensions['B'].width = 15

    output.seek(0)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
    return response


def append_kafiat_row(rows, s, kafiat_type):
    rows.append({
        "ردیف": None,
        "نام": s.name,
        "نام خانوادگی": s.family,
        "نام پدر": s.fathers_name,
        "کد ملی": s.National_Code,
        "امریه دار(*)": "دارد" if s.Amriye else "ندارد",
        "سازمان امریه": s.Amriye_organization if s.Amriye else "",
        "وضعیت جسمانی": s.physical_condition or "سالم",
        "نوع بیماری": s.Type_of_disease or "",
        "مقطع تحصیلی": s.educational_level_of_the_system,
        "مدرک 2": s.educational_level_of_the_system,
        "یگان خدمتی": s.yegan_name or "",
        "نوع کفایت": kafiat_type,
    })

def export_kafiat_to_excel(filename="kafiat"):
    rows = []

    for s in Soldier.objects.filter(has_been_accepted=True, Sufficiency_of_mobilization=True):
        append_kafiat_row(rows, s, "کفایت بسیج")

    for s in Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True):
        append_kafiat_row(rows, s, "کفایت دار خدمت قبلی")

    for l in NormalLetterModels.objects.filter(subject="معرفی به کمیسیون", soldire__the_medical_commission=True):
        s = l.soldire
        append_kafiat_row(rows, s, "معرفی به کمیسیون")

    for l in NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی", soldire__the_medical_commission=True):
        s = l.soldire
        append_kafiat_row(rows, s, "معرفی به کمیسیون شروع دوره آموزشی")
    
    for l in CheckoutLetterModels.objects.filter(c_type="تجدید دوره"):
        s = l.soldire
        append_kafiat_row(rows, s, "تجدید دوره")

    df = pd.DataFrame(rows)

    df["ردیف"] = range(1, len(df) + 1)

    df = df[
        ["ردیف", "نام", "نام خانوادگی", "نام پدر", "کد ملی",
         "امریه دار(*)", "سازمان امریه", "وضعیت جسمانی", "نوع بیماری",
         "مقطع تحصیلی", "مدرک 2", "یگان خدمتی", "نوع کفایت"]
    ]

    # ساخت فایل اکسل
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="فهرست-فراگیران")

        ws = writer.sheets["فهرست-فراگیران"]
        ws.sheet_view.rightToLeft = True  # راست‌چین

        # استایل فونت
        vazir_font = Font(name="Vazirmatn", size=12, bold=False)

        # استایل Border
        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin")
        )

        # استایل Alignment (وسط‌چین افقی و عمودی)
        center_align = Alignment(horizontal="center", vertical="center")

        # اعمال استایل روی تمام سلول‌ها (شامل هدر)
        for row in ws.iter_rows():
            for cell in row:
                cell.font = vazir_font
                cell.border = thin_border
                cell.alignment = center_align

        # تنظیم عرض ستون‌ها بر اساس بزرگ‌ترین متن
        for col in ws.columns:
            max_length = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    length = len(str(cell.value))
                    if length > max_length:
                        max_length = length
            adjusted_width = max_length + 2  # کمی فاصله اضافه
            ws.column_dimensions[col_letter].width = adjusted_width

    output.seek(0)
    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
    return response
