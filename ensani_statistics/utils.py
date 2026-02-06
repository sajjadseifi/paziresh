import re

DASH_REGEX = r'[‐-‒–—−-]'

def normalization_persian(value: str, remove_hidden_characters=True) -> str:
    if not value:
        return ""

    value = str(value)

    # 1️⃣ حروف عربی → فارسی
    value = (
        value.replace('ي', 'ی')
             .replace('ك', 'ک')
             .replace('ؤ', 'و')
             .replace('أ', 'ا')
             .replace('إ', 'ا')
    )


    if remove_hidden_characters:
        # 2️⃣ حذف کاراکترهای مخفی
        value = re.sub(r'[\u200c\u200f\u202a-\u202e]', '', value)

    # 5️⃣ تمیزکاری نهایی
    return value.strip()

def smart_separation(text):
    # 3️⃣ یکسان‌سازی فاصله‌ها
    value = re.sub(r'\s+', ' ', text)
    # 4️⃣ حذف هر چیزی بعد از اولین dash (هر نوع dash)
    value = re.split(DASH_REGEX, value, maxsplit=1)[0]

    return value