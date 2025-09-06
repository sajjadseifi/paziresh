import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from io import BytesIO
from .models import CheckoutLetterModels


def export_checkout_letters_to_excel(letters=None, filename='checkout_letters', sheet_name='نامه‌ها', include_stats=True):
    """
    letters: می‌تواند لیست یا QuerySet از CheckoutLetterModels باشد
    """
    if letters is None:
        letters = CheckoutLetterModels.objects.all().select_related("soldire").order_by("-create_time")
    elif isinstance(letters, list):
        # اگر لیست بود، از آن مستقیم استفاده می‌کنیم
        letters = letters
    else:
        # اگر QuerySet بود، select_related اضافه می‌کنیم
        letters = letters.select_related("soldire").order_by("-create_time")

    letters_list = []
    for obj in letters:
        letters_list.append({
            "number": obj.number,
            "c_type": obj.c_type,
            "status": obj.status,
            "create_time": obj.create_time.date(),
            "description": obj.description,
            "soldire__name": obj.soldire.name,
            "soldire__family": obj.soldire.family,
            "soldire__National_Code": obj.soldire.National_Code,
        })

    df = pd.DataFrame(letters_list)

    # تغییر نام ستون‌ها
    df.rename(columns={
        "number": "شماره نامه",
        "c_type": "علت نامه",
        "soldire__National_Code": "کد ملی",
        "soldire__name": "نام",
        "soldire__family": "نام خانوادگی",
        "status": "وضعیت",
        "create_time": "تاریخ",
        "description": "توضیحات",
    }, inplace=True)

    df = df[[
        "شماره نامه",
        "علت نامه",
        "کد ملی",
        "نام",
        "نام خانوادگی",
        "وضعیت",
        "تاریخ",
        "توضیحات"
    ]]
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        ws = writer.sheets[sheet_name]

        # استایل‌ها
        thin_border = Border(
            left=Side(style="thin", color="000000"),
            right=Side(style="thin", color="000000"),
            top=Side(style="thin", color="000000"),
            bottom=Side(style="thin", color="000000"),
        )
        header_fill = PatternFill(start_color="87CEEB", end_color="87CEEB", fill_type="solid")
        header_font = Font(name="Vazirmatn", bold=True, color="000000", size=13)
        content_font = Font(name="Vazirmatn", size=11)

        # استایل هدر
        for col_idx, column in enumerate(df.columns, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

        # استایل محتوای ردیف‌ها
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.font = content_font
                cell.border = thin_border

        ws.sheet_view.rightToLeft = True

        # عرض ستون‌ها
        for i, col in enumerate(df.columns, 1):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            ws.column_dimensions[get_column_letter(i)].width = max_length

        # شیت آمار
        if include_stats:
            ws2 = writer.book.create_sheet(title="آمار")
            total = len(df)
            approved = df[df["وضعیت"] == "تایید شده"].shape[0]
            rejected = df[df["وضعیت"] == "رد شده"].shape[0]
            waiting = df[(df["وضعیت"] != "تایید شده") & (df["وضعیت"] != "رد شده")].shape[0]

            stats = {
                "کل نامه‌ها": total,
                "تایید شده": approved,
                "رد شده": rejected,
                "در انتظار": waiting,
            }

            ws2.append(["عنوان", "تعداد"])
            for cell in ws2[1]:
                cell.fill = header_fill
                cell.font = Font(name="Vazirmatn", bold=True, size=13)
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = thin_border

            row_fill1 = PatternFill(start_color="E0FFFF", end_color="E0FFFF", fill_type="solid")
            row_fill2 = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

            for row_num, (key, value) in enumerate(stats.items(), 2):
                fill = row_fill1 if row_num % 2 == 0 else row_fill2

                ws2.cell(row=row_num, column=1, value=key).fill = fill
                ws2.cell(row=row_num, column=1).font = Font(name="Vazirmatn", size=12)
                ws2.cell(row=row_num, column=1).alignment = Alignment(horizontal="right", vertical="center")
                ws2.cell(row=row_num, column=1).border = thin_border

                ws2.cell(row=row_num, column=2, value=value).fill = fill
                ws2.cell(row=row_num, column=2).font = Font(name="Vazirmatn", size=12)
                ws2.cell(row=row_num, column=2).alignment = Alignment(horizontal="center", vertical="center")
                ws2.cell(row=row_num, column=2).border = thin_border

            ws2.sheet_view.rightToLeft = True
            ws2.column_dimensions["A"].width = 25
            ws2.column_dimensions["B"].width = 15

    output.seek(0)
    response = HttpResponse(
        output, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename={filename}.xlsx"
    return response
