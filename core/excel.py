# code/excel.py

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from django.http import HttpResponse
import datetime

def generate_excel(headers, data, filename="export.xlsx"):
    """
    تولید اکسل با استایل RTL، هدر بزرگ و آماده‌سازی برای دانلود

    :param headers: لیست هدرها ['ستون1', 'ستون2', ...]
    :param data: لیست داده‌ها [[row1col1, row1col2,...], [row2col1,...], ...]
    :param filename: نام فایل خروجی
    :return: HttpResponse برای دانلود اکسل
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "اطلاعات"
    ws.sheet_view.rightToLeft = True

    # استایل‌ها
    header_font = Font(name="Tahoma", bold=True, color="FFFFFF", size=14)  # بزرگتر
    header_fill = PatternFill("solid", fgColor="4F81BD")
    header_align = Alignment(horizontal="center", vertical="center")  # راست‌چین

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # اضافه کردن هدر
    for col_num, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border

    # افزایش ارتفاع ردیف هدر برای padding بیشتر
    ws.row_dimensions[1].height = 25  # می‌توانید عدد را تغییر دهید

    # اضافه کردن داده‌ها
    for row_num, row in enumerate(data, start=2):
        for col_num, value in enumerate(row, start=1):
            cell = ws.cell(row=row_num, column=col_num, value=value)
            cell.alignment = Alignment(horizontal="center", vertical="center")  # راست‌چین
            cell.font = Font(name="Tahoma", size=12)  # کمی کوچکتر از هدر
            cell.border = thin_border

    # Auto width برای ستون‌ها
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column].width = max_length + 5

    # آماده‌سازی HttpResponse برای دانلود
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    response['Content-Disposition'] = f'attachment; filename={filename.replace(".xlsx", "")}_{now}.xlsx'

    wb.save(response)
    return response
