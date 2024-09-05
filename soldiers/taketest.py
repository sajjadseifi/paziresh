# Workbook را باز کنید
import xlrd

exel = 'lst_of_yegan.xlsx'
workbook = xlrd.open_workbook(exel)

# شیت مورد نظر خود را انتخاب کنید (مثلاً شیت اول)
sheet = workbook.sheet_by_index(0)

# تعداد ردیف‌ها و ستون‌های شیت را بدست آورید
num_rows = sheet.nrows
num_cols = sheet.ncols
# برای هر سطر
for row_idx in range(1, num_rows):
    one_soldire_list = []
    for col_idx in range(num_cols):
        # مقدار سلول را بخوانید
        cell_value = sheet.cell_value(row_idx, col_idx)
        # مقدار دهی به لیست
        if str(cell_value).find('ي'):
            cell_value = str(cell_value).replace('ي', 'ی')
        if str(cell_value).find('ك'):
            cell_value = str(cell_value).replace('ك', 'ک')
        if str(cell_value).find('ك'):
            cell_value = str(cell_value).replace('ؤ', 'و')
        one_soldire_list.append(cell_value)

    print(one_soldire_list)
