from .constants import educational_level_of_the_system_list,Grade_precise_list
def generate_grade_temp(educational_level_of_the_system):
    temp = 0
    for i in educational_level_of_the_system_list:
        i1 = i[1].replace(" ", "").replace("\u200c", "")
        nv =  educational_level_of_the_system.replace(" ", "").replace("\u200c", "")
        if i1 == nv:
            temp = i[0]
            
    return temp

def categorize_educational_level(level_id):
    if level_id in {14, 15, 16, 17, 18, 27, 29, 30, 31, 32, 33, 19, 20, 34, 21, 22, 35, 36, 23, 24, 37, 38}:
        return 1, 'زیر دیپلم'
    elif level_id in {25, 26, 39, 13, 44}:
        return 2, 'دیپلم'
    elif level_id in {4, 5, 6, 42}:
        return 3, 'فوق دیپلم'
    elif level_id in {9, 10, 11, 12, 1, 40, 41}:
        return 4, 'لیسانس'
    elif level_id in {7, 8, 45}:
        return 5, 'فوق لیسانس'
    elif level_id in {2, 3, 43, 3}:
        return 6, 'دکتری'
    elif level_id == 0:
        return 7, 'نامشخص'
    else:
        return 7, 'نامشخص'


def map_educational_level_to_grade(level):
    grade_precise_mapping = {
        'بی‌سواد': [],
        'نهضت سواد آموزی': [],
        'ابتدایی': [14, 15, 16, 17, 18, 27, 29, 30, 31, 32, 33],
        'راهنمایی': [19, 20, 34],
        'سیکل': [21, 22, 35, 36],
        'دبیرستان': [23, 24, 37, 38],
        'زیر دیپلم': [],
        'دیپلم': [25, 26, 39, 13, 44],
        'فوق دیپلم': [4, 5, 6, 42],
        'لیسانس': [9, 10, 11, 12, 1, 40, 41],
        'فوق لیسانس': [7, 8, 45],
        'دکتری': [2, 3, 43],
        'نامشخص': [0]
    }

    for grade_level, grade_name in Grade_precise_list:
        if level in grade_precise_mapping[grade_name]:
            return grade_level, grade_name

    return None