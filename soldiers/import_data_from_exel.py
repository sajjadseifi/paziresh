# from soldiers.models import Soldier
# import openpyxl
#
# # بارگذاری فایل اکسل
# exel = 's.xlsx'
# workbook = openpyxl.load_workbook(exel)
#
# # انتخاب شیت اول
# sheet = workbook.active
#
# # بدست آوردن تعداد ردیف‌ها و ستون‌ها
# num_rows = sheet.max_row
# num_cols = sheet.max_column
#
# # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
# for row_idx in range(2, num_rows + 1):
#     one_soldire_list = []
#     for col_idx in range(1, num_cols + 1):
#         # مقدار سلول را بخوانید
#         cell_value = sheet.cell(row=row_idx, column=col_idx).value
#         if cell_value is not None:
#             # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
#             cell_value = str(cell_value)
#             cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و')
#         one_soldire_list.append(cell_value)
#     print(one_soldire_list[0])
#     if str(one_soldire_list[0]) == "null":
#         find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
#         if find_soldire is not None:
#             print(find_soldire.name)
