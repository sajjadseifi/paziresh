from django.shortcuts import render
from django.views import View

from ensani_soldires_management.forms import FormUpdateGordan, Formjazbi, FormYegankhedmati, \
    FormUpdateAllSoldiresHasbenAceptedInCourse, FormUpdateAllSoldires
from soldiers.models import Soldier
from ensani_letter.models import NormalLetterModels
import pandas as pd
from django.http import HttpResponse
import openpyxl
from battalions.models import battalion, battalion_group

list_yegan_bekargirande = [
    (1, 'تیپ نینوا', 'سپاه و رده های اقماری', 'گلستان', 'گرگان- جاده شصت کلاته- پادگان شهید مصطفی خمینی'),
    (2, 'سپاه نینوا - گلستان', 'سپاه و رده های اقماری', 'گلستان', 'گلستان-گرگان-فلکه بسیج'),
    (3, 'سپاه قدس - گیلان', 'سپاه و رده های اقماری', 'گیلان', 'رشت- یخ سازی - شهدای گمنام - سپاه قدس گیلان'),
    (4, 'قرارگاه بازسازی خاتم الانبیاء (ص)', 'نقسا', 'تهران',
     'تهران-اتوبان افسریه-انتهای هجرت(مرکز شهید پازوکی) قرارگاه مهندسی و بازسازی خاتم الانبیا'),
    (5, 'سازمان جنگال سپاه', 'سپاه و رده های اقماری', 'تهران',
     'بلوار هجرت-روبروی پادگان 02 ارتش-خ شهید تجاره-سه راه تختی'),
    (6, 'نمایندگی ولی فقیه درسپاه', 'حوزه نمایندگی', 'تهران',
     'بزرگراه بسیج-جنب شهرک کلاهدوز-خ وحدت - پادگان شهید میثمی'),
    (7, 'دانشگاه افسری و تربیت پاسداری امام حسین (ع)', 'سپاه و رده های اقماری', 'تهران',
     'تهران-اتوبان شهید بابائی-ابتدای جاده لواسان'),
    (8, 'مرکز عملیات نیروی انسانی سپاه', 'سپاه و رده های اقماری', 'تهران',
     'تهران-اتوبان بسیج-سه راه تختی-بلوار هجرت-درب شهید فیاض بخش'),
    (9, 'نامشخص', 'نامشخص', '***', '******'),
    (10, 'معاونت مهندسی و پدافند غیر عامل', 'سپاه و رده های اقماری', 'تهران',
     'تهران-اتوبان بسیج-سه راه تختی-بلوار هجرت -درب فیاض'),
    (11, 'فرماندهی حفاظت و امنیت سپاه', 'سپاه و رده های اقماری', 'تهران',
     'تهران-میدان پاستور-روبروی ساختمان حفاظت ولی امر-ساختمان انصار'),
    (12, ' کوثر ولایت', 'سپاه و رده های اقماری', 'تهران',
     'تهران-اتوبان بسیج-بلوار هجرت(شهدای سرباز)-میدان شهید مطهری-انتهای خیابان شهید آتوت-مقر شهید مطهری'),
    (13, 'سازمان بسیج مستضعفین', 'سازمان بسیج', 'تهران',
     'تهران-اتوبان بسیج-روبروی خ شهید محلاتی(آهنگ)-مدیریت نیروی انسانی'),
    (14, 'دانشگاه جامع امام حسین (ع)', 'سپاه و رده های اقماری', 'تهران', 'تهران -انتهای اتوبان شهید بابائی'),
    (15, 'معاونت نیروی انسانی نیروی هوافضا', 'سپاه و رده های اقماری', 'تهران',
     'تهران-جنب پارک چیتگر-خیابان کوهک-ستاد نیروی هوایی سپاه'),
    (16, 'گروه پدافندهوایی 10 محرم نزسا', 'نزسا', 'سمنان', 'سمنان-شاهرود-کیلومتر 10 جاده شاهرود-مجن'),
    (17, 'سپاه قائم آل محمد (عج) - سمنان', 'سپاه و رده های اقماری', 'سمنان', 'سمنان-میدان جهاد-جاده کمربندی'),
    (18, 'سپاه کربلا - مازندران', 'سپاه و رده های اقماری', 'مازندران', 'ساری-میدان خزر-سپاه کربلا'),
    (19, 'آموزشگاه المهدی (عج) نزسا', 'نزسا', 'مازندران', 'بابل-بندپی غربی-خوشرودپی'),
    (20, 'قرارگاه عملیاتی ثاراله', 'سپاه و رده های اقماری', 'تهران',
     'خیابان ولیعصر-بزرگراه نیایش-چهارراه سئول-جنب ورزشگاه انقلاب'),
    (21, 'معاونت بهداری رزمی نیروی زمینی سپاه', 'نزسا', 'تهران',
     'تهران-بزرگراه بسیج-سه راه تختی-بلوار هجرت- ستاد نیروی زمینی سپاه'),
    (22, 'بنیاد تعاون', 'سپاه و رده های اقماری', 'تهران',
     'تهران-بزرگراه نیایش-ابتدای خیابان سئول شمالی-جنب فدراسیون هندبال'),
    (23, 'لشکر 16 قدس', 'سپاه و رده های اقماری', 'گیلان', '******'),
    (24, 'معاونت فن آوری اطلاعات و ارتباطات', 'سپاه و رده های اقماری', 'تهران',
     'تهران- بزرگراه بسیج سه راه تختی بلوار هجرت-بعد از دژبان کل سپاه معاونت فاوا کل سپاه پادگان بقیه الله'),
    (25, 'تیپ نیروی مخصوص میرزا کوچک خان نزسا', 'نزسا', 'گیلان', 'گیلان-لنگرود-تیپ تکاور میرزا'),
    (26, 'فرماندهی پشتیبانی و اجرائیات حوزه مرکزی', 'سپاه و رده های اقماری', 'تهران',
     'تهران -سه را تختی-بلوار هجرت درب اصلی روبروی پدافند هوایی'),
    (27, 'معاونت آماد و پشتیبانی سپاه', 'سپاه و رده های اقماری', 'تهران',
     'تهران-کیلومتر 9 جاده قدیم کرج -بعد از سه راه شهریار-پادگان حضرت ابوالفضل(ع)'),
    (28, 'سپاه سیدالشهداء (ع) - استان تهران', 'سپاه و رده های اقماری', 'تهران',
     'تهران-شهر ری-میدان نماز-خیابان امام حسین(ع)-ستاد فرماندهی سپاه سیدالشهدا(ع)'),
    (29, 'معاونت مهندسی نیروی زمینی سپاه', 'نزسا', 'تهران', 'بلوار هجرت-میدان شهید باکری-معاونت مهندسی نزسا'),
    (30, 'آمادگاه مهماتی شهید هاشمی نژاد', 'نزسا', 'سمنان', 'دامغان-جاده اصفهان(معلمان جندق) کیلومتر 40-سمت راست'),
    (31, 'سپاه امام حسن مجتبی(ع) - استان البرز', 'سپاه و رده های اقماری', 'البرز',
     'کرج-میدان سپاه-پادگان شرع پسند-سپاه امام حسن مجتبی(ع)'),
    (32, 'گروه 45 مهندسی جواد الائمه نزسا', 'نزسا', 'گلستان', 'گرگان-روستای جعفرآباد'),
    (33, 'تیپ نیروی مخصوص 110 سلمان فارسی نزسا', 'نزسا', 'سیستان و بلوچستان',
     'کمربندی شهید کلانتری - انتهای بلوار سرداران شهید'),
    (34, 'قرارگاه منطقه ای قدس (جنوبشرق) نزسا', 'نزسا', 'سیستان و بلوچستان', 'زاهدان - میدان آزادی - قرارگاه قدس'),
    (35, 'ستاد کل نیروهای مسلح', 'ستاد کل نیروهای مسلح', 'تهران', 'تهران-میدان سبلان-نبش میدان-پادگان شهید نظران'),
    (36, 'سپاه جوادالائمه (ع) - خراسان شمالی', 'سپاه و رده های اقماری', 'خراسان شمالی',
     'خراسان شمالی-بجنورد-بلوار پیامبر اعظم(ص)-جنب پزشکی قانونی-ستاد سپاه حضرت جوادالائمه(ع)'),
    (37, 'تیپ حضرت جواد(ع)', 'سپاه و رده های اقماری', 'خراسان شمالی',
     'بجنورد-کیلومتر 17 کمربندی گستان شهر-روستای لنگر-پادگان شهید نوری'),
    (38, 'یگان زرهی 60 عمار نزسا', 'نزسا', 'گلستان',
     'گنبد کاووس-جاده کمربندی مشهد گنبد-شهرک بهارستان-پادگان شهید اسودی'),
    (39, 'گروه 46 مهندسی امام هادی(ع) نزسا', 'نزسا', '******', '******'),
    (40, 'تیپ نیروی ویژه صابرین نزسا', 'نزسا', 'تهران',
     'تهران - اتوبان افسریه - 3راه تختی - میدان مطهری - تیپ نیروی ویژه صابرین'),
    (41, 'آموزشگاه شهید هاشمی نژاد شیروان نزسا', 'نزسا', 'خراسان شمالی', 'شیروان-روستای دامغان'),
    (42, 'سپاه امام رضا (ع) - خراسان رضوی', 'سپاه و رده های اقماری', 'خراسان رضوی', 'مشهد-انتهای بلوار وکیل آباد'),
    (43, 'قرارگاه عملیاتی منطقه ای غدیر نزسا', 'نزسا', 'مازندران', 'مازندران-ساری-میدان امام'),
    (44, 'سپاه انصارالمهدی (عج) - زنجان', 'سپاه و رده های اقماری', 'زنجان', 'زنجان-سه راه امجدیه-سپاه انصارالمهدی(عج)'),
    (45, 'ندسا-بیمارستان32 تختخوابی شهید محمدیها لنگه', 'ندسا', 'هرمزگان', 'استان هرمزگان-بندر لنگه-بعد از گمرک'),
    (46, 'گروه توپخانه 61 محرم نزسا', 'نزسا', 'خراسان رضوی', 'خراسان رضوی-تربت حیدریه-کیلومتر 10 جاده تربت حیدریه'),
    (47, 'لشکر 5 نصر', 'سپاه و رده های اقماری', 'خراسان رضوی',
     'مشهد- ابتدای جاده قدیم نیشابور- جنب شهرک ابوذر- لشگر  5نصر'),
    (48, 'مرکز 203 جوادالائمه (ع) نزسا', 'نزسا', '******', '******'),
    (49, 'مرکز جنگال فاطر نزسا', 'نزسا', 'تهران', '******'),
    (50, 'قرارگاه منطقه ای ثامن الائمه (ع) (شمالشرق) نزسا', 'نزسا', 'خراسان رضوی', '******'),
    (51, 'فرماندهی دژبان کل سپاه', 'سپاه و رده های اقماری', 'تهران', 'تهران-بلوار هجرت-فرماندهی دژبان کل سپاه'),
    (52, 'گروه 47 مهندسی سلمان نزسا', 'نزسا', 'خراسان رضوی',
     'خراسان رضوی-سبزوار-کیلومتر 5 جاده قدیم-پادگان شهید فرومندی'),
    (53, 'مرکز بهداری رزمی شمال شرق نزسا', 'نزسا', '******', '******'),
    (54, 'مرکز فناوری ارتباطات واطلاعات ثامن الائمه (ع) نزسا', 'نزسا', 'تهران', '******'),
    (55, 'نمایندگی ولی فقیه در نیروی زمینی سپاه', 'حوزه نمایندگی', 'تهران',
     'تهران-اتوبان بسیج -سه راه تختی-بلوار هجرت-پادگان صفوی'),
    (56, ' آمادگاه مهمات شهید باهنر نزسا', 'نزسا', '******', '******'),
    (57, 'مرکز خدمات رفاهی و کارکنان نیروی زمینی سپاه ', 'نزسا', 'تهران',
     'تهران-اتوبان بسیج-سه راه تختی-بلوار هجرت-میدان مطهری'),
    (58, 'تیپ زرهی 21 امام رضا (ع) نزسا', 'نزسا', 'خراسان رضوی', '******'),
    (59, 'سپاه سلمان - سیستان و بلوچستان', 'سپاه و رده های اقماری', 'سیستان و بلوچستان',
     'زاهدان - جاده کمربندی شهید کلانتری نرسیده به ترمینال انقلاب'),
    (60, 'سپاه علی ابن ابیطالب (ع) - قم', 'سپاه و رده های اقماری', 'قم', 'قم- فلکه 72تن پادگان امام صادق)ع'),
    (61, 'مرکز بهداری جنوب شرق نزسا', 'نزسا', '******', '******'),
    (62, 'سپاه شهدا - آذربایجان غربی', 'سپاه و رده های اقماری', 'آذربایجان غربی',
     'ارومیه خ شهید بهشتی چهارراه دانشکده پشت پمپ بنزین سپاه شهدا'),
    (63, 'آمادگاه ابوذر سبزوار', 'سپاه و رده های اقماری', 'خراسان رضوی', 'میدان شریعتی-میدان خلیج فارس-بلوار ابوذر'),
    (64, 'مرکز عملیات نیروی انسانی نیروی زمینی سپاه ', 'نزسا', 'تهران',
     'تهران-اتوبان بسیج-سه راه تختی-انتهای بلوار هجرت-میدان شهید مطهری-معاونت نیروی انسانی نزسا'),
    (65, 'آمادگاه مهمات مقداد نزسا', 'نزسا', 'خراسان رضوی', 'خراسان رضوی - نیشابور - 45کیلومتری جاده نیشابور'),
    (66, 'سپاه الغدیر - یزد', 'سپاه و رده های اقماری', 'یزد', 'یزد -بلوار جانباز سپاه الغدیر استان یزد'),
    (67, 'مرکز خدمات کارکنان سپاه', 'سپاه و رده های اقماری', 'تهران',
     'تهران-بزرگراه نیایش-ابتدای خیابان سئول شمالی-جنب فدراسیون هندبال'),
    (68, 'ندسا - دانشگاه امام خامنه ای', 'ندسا', 'مازندران', '3 راه حسن رود- زیباکنار'),
    (69, 'آموزشگاه شهید باکری نزسا', 'نزسا', 'خوزستان', '******'),
    (70, 'سپاه ولیعصر (عج) - خوزستان', 'سپاه و رده های اقماری', 'خوزستان',
     'خوزستان-اهواز-چهارشیر-نبش بیمارستان ابوذر-سپاه حضرت ولیعصر)عج(استان'),
    (71, 'تیپ مکانیزه 20 رمضان نزسا', 'نزسا', 'تهران', 'اتوبان تهران قم - جنب شهرک سینمایی - پادگان شهید نوری'),
    (72, 'فرماندهی قرارگاه مرکزی امام حسین ع', 'سپاه و رده های اقماری', 'تهران',
     'تهران-اتوبان بسیج-سه راه تختی-بلوار هجرت- درب فیاض'),
    (73, 'فرماندهی پشتیبانی و اجرائیات حوزه مرکزی ستاد فرماندهی کل سپاه - قرارگاه فرهنگی بقیه الله الاعظم عج',
     'سپاه و رده های اقماری', 'تهران',
     'تهران-خیابان شریعتی-بالاتر از حسینیه ارشاد-روبروی بیمارستان مفید-کوچه بهشت آسا-پلاک 1/6'),
    (74, 'سپاه حضرت عباس (ع) - اردبیل', 'سپاه و رده های اقماری', 'اردبیل', 'اردبیل میدان بسیج'),
    (75, 'گروه پهباد نزسا', 'نزسا', 'تهران',
     'تهران-پهپاد-بعد از سه راه شهریار-خیابان سپاه اسلام-پادگان صاحب الزمان(عج)'),
    (76, 'آموزشگاه شهید مدرس نزسا', 'نزسا', 'البرز', 'کیلومتر 20 تهران کرج-جنب شهرک خاتم-آموزشگاه مدرس'),
    (77, 'فرماندهی هوانیروز نزسا', 'نزسا', 'تهران',
     'سه راه تختی-بلوار هجرت-جنب معاونت بهداری رزمی نزسا-فرماندهی هوانیروز'),
    (78, 'فرماندهی هوانیروز سپاه (گروه بالگردی فتح) نزسا', 'نزسا', 'البرز', 'کرج-مشکین دشت-به سمت روستای خوشنام'),
    (79, 'سپاه صاحب الامر (عج) - قزوین', 'سپاه و رده های اقماری', 'قزوین', 'قزوین - ابتدای کوثر- مقابل مجتمع میلاد'),
    (80, 'نامعلوم', 'نامعلوم', '***', '******'),
    (81, 'آموزشگاه شهید قاضی طباطبائی نزسا', 'نزسا', 'آذربایجان شرقی', 'تبریز-کیلومتر 25 جاده آذرشهر'),
    (82, 'سپاه حضرت محمد رسول اله (ص) - تهران بزرگ', 'سپاه و رده های اقماری', 'تهران', 'میدان سپاه-پادگان ولیعصر(عج)'),
    (83, 'موقعیت امام هادی (ع)', 'سپاه و رده های اقماری', 'تهران',
     'تهران-بزرگراه بسیج-بزرگراه شهید دوران-جنب مقبره شهدا-نیروی دریایی سابق'),
    (84, 'قرارگاه سازندگی خاتم الانبیاء (ص)', 'نقسا', 'تهران', 'شهرک غرب -بلوار ایوانک-ضلع شمالی-چهارراه فلامک'),
    (85, 'ندسا-بیمارستان صاحب الزمان (عج) و مرکز بهداری جنوب ', 'ندسا', 'هرمزگان',
     'استان هرمزگان-بندرعباس-سه راه هتل هما'),
    (86, 'سپاه بیت المقدس - کردستان', 'سپاه و رده های اقماری', 'کردستان',
     'کردستان-شهرستان سنندج-خ امام خمینی(ره)-میدان ارتش'),
    (87, 'فرماندهی آمادگاه نگهداری مهمات مصطفی خمینی ( قم )', 'سپاه و رده های اقماری', 'قم',
     'دریافت آدرس از اداره سرباز'),
    (88, 'ندسا- مجتمع بهداشتی درمانی سیدالشهداء(ع) چابهار', 'ندسا', 'سیستان و بلوچستان',
     'استان سیستان و بلوچستان-چابهار-جنب منطقه ویژه اقتصادی'),
    (89, 'سازمان تحقیقات وخودکفایی نیروی زمینی سپاه ', 'نزسا', 'تهران',
     'تهران-سه راه تختی - بعد از میدان شهید باکری-سازمان تحقیقات و خودکفایی'),
    (90, 'قرارگاه منطقه ای صاحب الزمان  (عج)  نزسا', 'نزسا', 'تهران',
     'تهران-سه راه تختی-انتهای بلوار هجرت-میدان شهید باکری-جنب ستاد نیروی زمینی سپاه-روبروی معاونت بهداری'),
    (91, 'ستاد نیروی زمینی سپاه - پادگان شهید صفوی ', 'نزسا', 'تهران',
     'تهران-سه راه تختی-انتهای بلوار هجرت-میدان شهید باکری-پادگان شهید صفوی'),
    (92, 'آموزشگاه درجه داری سیدالشهدا (ع) نزسا', 'نزسا', 'آذربایجان شرقی', 'تبریز-آذرشهر-جاده ارومیه'),
    (93, 'ندسا- بیمارستان شهید سلیمانی', 'ندسا', 'بوشهر', 'استان بوشهر-عسلویه-چاه مبارک'),
    (94, 'مرکز آموزش عالی هوانوردی نزسا', 'نزسا', 'البرز', 'کرج-مشکین دشت به سمت خوشنام-سر شهرک ناز-مرکز آموزش'),
    (95, 'آموزشگاه مالک اشتر نزسا', 'نزسا', 'آذربایجان غربی', 'ارومیه-جاده دریا-آموزشگاه مالک اشتر'),
    (96, 'ندسا-بیمارستان امام رضا(ع) چالوس', 'ندسا', 'مازندران', 'مازندران-چالوس-جنب مخابرات'),
    (97, 'دانشگاه علوم پزشکی بقیه الله الاعظم (عج)', 'سپاه و رده های اقماری', 'تهران',
     'تهران- میدان ونک ابتدای خیابان ملاصدرا'),
    (98, 'ندسا - معاونت نیروی انسانی', 'ندسا', 'بندرعباس',
     'بندرعباس-جنب اسکله شهید باهنر-ستاد نیروی دریایی سپاه-معاونت نیروی انسانی ندسا'),
    (99, 'معاونت فاوا نیروی زمینی سپاه', 'نزسا', 'تهران',
     'بلوار هجرت - انتهای خیابان آتوت - جنب تیپ نیروی ویژه صابرین'),
    (100, 'سپاه ولی امر', 'سپاه و رده های اقماری', 'تهران', 'تهران-خ کارگر جنوبی-میدن پاستور-مقر شهیدان مداح'),
    (101, 'دفتر معاونت نیروی انسانی سپاه', 'سپاه و رده های اقماری', 'تهران',
     'سه راه تختی-بلوار هجرت -بعد از میدان فتح المبین- موقعیت شهید زین الدین'),
    (102, 'ندسا - پایگاه دریائی شمال ', 'ندسا', 'مازندران', 'بابلسر- جنب شهرک دریا کنار - روبروی مجتمع پرشیا'),
    (103, 'ندسا-بیمارستان قائم(عج) و مرکز بهداری شمال خلیج فارس', 'ندسا', 'بوشهر',
     'استان بوشهر بوشهر میدان امام خیابان بی سیم جنب سپاه امام صادق )ع('),
    (104, 'ندسا - منطقه دوم ', 'ندسا', 'بوشهر', 'بوشهر- سهراهی امامزاده پادگان نوح نبی)ع-(منطقه دوم ندسا'),
    (105, 'معاونت اطلاعات نیروی زمینی سپاه ', 'نزسا', 'تهران',
     'تهران سه راه تختی-انتهای بلوار هجرت.میدان شهید باکری - پادگان شهید صفوی -معاونت اطلاعات'),
    (106, 'معاونت آماد و پشتیبانی ندسا', 'ندسا', '******', '******'),
    (107, 'سپاه انصارالرضا (ع) - خراسان جنوبی', 'سپاه و رده های اقماری', 'خراسان جنوبی',
     'استان خراسان جنوبی-بیرجند-بلوار پیامبر اعظم )ص-(میدان سپاه ستاد سپاه استان'),
    (108, 'سپاه صاحب الزمان (عج) - اصفهان', 'سپاه و رده های اقماری', 'اصفهان',
     'اصفهان- سه راه حکیم نظامی خیابان شهدای صفه'),
    (109, 'ندسا-بیمارستان32 تختخوابی شهید عمویی ماهشهر', 'ندسا', 'خوزستان', 'استان خوزستان - شهرستان بندرماهشهر-فاز2'),
    (110, 'مرکز آموزش تخصصی جنوب شرق نزسا', 'نزسا', 'سیستان و بلوچستان', 'زاهدان-کیلومتر  5جاده زاهدان بم'),
    (111, 'ندسا - سازمان تحقیقات و خودکفایی', 'ندسا', 'تهران',
     'تهران-اتوبان شهیدعباس دوران روبروی میدان تره بارپیروزی'),
    (112, 'ندسا - منطقه سوم ', 'ندسا', 'خوزستان', 'ماهشهر-پادگان دریایی امام حسین)ع'),
    (113, 'ندسا - منطقه چهارم دریایی ثارالله', 'ندسا', '******', '******'),
    (114, 'پایگاه شهید کاظمی(ارومیه)-نزسا', 'نزسا', '******', '******'),
    (115, 'سپاه عاشورا - آذربایجان شرقی', 'سپاه و رده های اقماری', '******', '******'),
    (116, 'بیمارستان  شهید صدوقی نزسا', 'نزسا', '******', '******')]


# Create your views here.


def soldier_search(request):
    query = request.GET.get('name')
    family = request.GET.get('family')
    national_code = request.GET.get('national_code')
    physical_condition = request.GET.get('physical_condition')
    marital_status = request.GET.get('marital_status')
    religion = request.GET.get('religion')
    acceptance_code = request.GET.get('acceptance_code')

    soldiers = Soldier.objects.all()

    if query:
        soldiers = soldiers.filter(name__icontains=query)
    if family:
        soldiers = soldiers.filter(family__icontains=family)
    if national_code:
        soldiers = soldiers.filter(National_Code__icontains=national_code)
    if physical_condition:
        soldiers = soldiers.filter(physical_condition__icontains=physical_condition)
    if marital_status:
        soldiers = soldiers.filter(marital_status=marital_status)
    if religion:
        soldiers = soldiers.filter(Religion__icontains=religion)
    if acceptance_code:
        soldiers = soldiers.filter(acceptance_code=acceptance_code)

    context = {
        'results': soldiers
    }

    return render(request, 'ensani_soldires_management/soldier_search.html', context)


def soldire_details(request, code):
    if request.method == "GET":
        soldire = Soldier.objects.filter(National_Code=code).first()
        normalLetter = NormalLetterModels.objects.filter(soldire=soldire).all()
        context = {'soldier': soldire, 'normalLetter': normalLetter}
        return render(request, 'ensani_soldires_management/soldire_details.html', context)


def export_to_excel_list_hazer_be_khdmat(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'acceptance_code', 'name', 'family',
        'National_Code', 't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai').order_by(
        'acceptance_code')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'acceptance_code': 'کد پذیرش',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'National_Code': 'کدملی',
        't_Gordan__name': 'نام گردان',
        't_battalion_group__name': 'نام گروهان',
        'code_gorhan_nahai': 'کد گروهان'
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_hazer_be_khdmat.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


def export_to_excel_list_sarbaz_tatbigh_nashode(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, in_coures=True, the_medical_commission=False,
                                      Previous_service_record=False, Sufficiency_of_mobilization=False,
                                      tatbigh=False, IsCheckout=False).values(
        'acceptance_code', 'name', 'family',
        'National_Code', 'Gordan__name', 'battalion_group__name', 't_Gordan__name', 't_battalion_group__name',
        'code_gorhan_nahai').order_by(
        'acceptance_code')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'acceptance_code': 'کد پذیرش',
        'name': 'نام',
        'family': 'نام خانوادگی',
        'National_Code': 'کدملی',
        'Gordan__name': 'نام گردان',
        'battalion_group__name': 'نام گروهان',
        't_Gordan__name': 'نام گردان جدید',
        't_battalion_group__name': 'نام گروهان جدید',
        'code_gorhan_nahai': 'کد گروهان جدید'
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_tatbigh_nashode.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


class exel_update_gordan(View):
    def get(self, request):
        form = FormUpdateGordan()
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_gordan.html', cx)

    def post(self, request):
        form = FormUpdateGordan(request.POST, request.FILES or None)
        cx = {'form': form}

        if form.is_valid():
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و')
                    one_soldire_list.append(cell_value)
                if one_soldire_list[0] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if find_soldire is not None:
                        t_gordan = battalion.objects.filter(name__icontains=one_soldire_list[7]).first()
                        t_gorohan = battalion_group.objects.filter(gordan=t_gordan,
                                                                   name__icontains=one_soldire_list[8]).first()
                        find_soldire.t_Gordan = t_gordan
                        find_soldire.t_battalion_group = t_gorohan
                        code_nahai_gorohan = one_soldire_list[9]
                        find_soldire.code_gorhan_nahai = int(code_nahai_gorohan)
                        find_soldire.tatbigh = True
                        find_soldire.save()

        return render(request, 'ensani_soldires_management/update_gordan.html', cx)


class exel_jazbi(View):
    def get(self, request):
        form = Formjazbi()
        form.fields['type'].choices = [("سپاه/مامور", 'سپاه/مامور'), ("نزسا", "نزسا"), ("موفق", "موفق")]
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_jazbi.html', cx)

    def post(self, request):
        form = Formjazbi(request.POST, request.FILES or None)
        form.fields['type'].choices = [("سپاه/مامور", 'سپاه/مامور'), ("نزسا", "نزسا"), ("موفق", "موفق")]
        cx = {'form': form}

        if form.is_valid():
            type = form.cleaned_data['type']
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و')
                    one_soldire_list.append(cell_value)
                if one_soldire_list[0] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if find_soldire is not None:
                        if type == "موفق":
                            find_soldire.Successful_recruitment = True
                            find_soldire.save()
                        else:
                            find_soldire.attraction_of_the_organization = type
                            find_soldire.save()

        return render(request, 'ensani_soldires_management/update_jazbi.html', cx)


def export_to_excel_list_sarbvaz_test_salamat_ravan(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                      physical_condition="سالم", attraction_of_the_organization='هیچکدام').values(
        'acceptance_code', 'name', 'family',
        'National_Code', 't_Gordan__name', 't_battalion_group__name',
        'code_gorhan_nahai').order_by(
        'acceptance_code')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'National_Code': 'کدملی',
        'name': 'نام',
        'family': 'نام خانوادگی',
        't_Gordan__name': 'نام گردان جدید',
        't_battalion_group__name': 'نام گروهان جدید',
        'code_gorhan_nahai': 'کد گروهان جدید'
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_test_salamt_ravan.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


def export_to_excel_list_sarbaz_be_sorat_gorohi(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'acceptance_code', 'name', 'family',
        'National_Code', 't_Gordan__name', 't_battalion_group__name',
        'code_gorhan_nahai').order_by(
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'acceptance_code': 'عدد پذیرش',
        'National_Code': 'کدملی',
        'name': 'نام',
        'family': 'نام خانوادگی',
        't_Gordan__name': 'نام گردان جدید',
        't_battalion_group__name': 'نام گروهان جدید',
        'code_gorhan_nahai': 'کد گروهان جدید'
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_goran_gorohani_codenahai.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


def import_exel_yegan_be_kar_girande(request):
    # بارگذاری فایل اکسل
    exel = 'D:/unittest/ensaniapp/soldiers/s.xlsx'
    workbook = openpyxl.load_workbook(exel)

    # انتخاب شیت اول
    sheet = workbook.active

    # بدست آوردن تعداد ردیف‌ها و ستون‌ها
    num_rows = sheet.max_row
    num_cols = sheet.max_column

    # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
    for row_idx in range(2, num_rows + 1):
        one_soldire_list = []
        for col_idx in range(1, num_cols + 1):
            # مقدار سلول را بخوانید
            cell_value = sheet.cell(row=row_idx, column=col_idx).value
            if cell_value is not None:
                # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                cell_value = str(cell_value)
                cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و')
            one_soldire_list.append(cell_value)
        if one_soldire_list[0] is not None:
            find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
            if find_soldire is not None:
                unit_name = str(one_soldire_list[1])
                unit_type = str(one_soldire_list[2])
                find_soldire.unit_type = unit_type
                find_soldire.unit_name = unit_name
                find_soldire.IsUnit = True
                find_soldire.save()
    return HttpResponse("S")


def PrintPosheNokhodi(request):
    in_course_soldire = Soldier.objects.filter(in_coures=True, willing_to_learn=True).order_by('t_Gordan__name',
                                                                                               't_battalion_group__name',

                                                                                               'code_gorhan_nahai')
    cx = {'soldires': in_course_soldire}
    return render(request, 'ensani_soldires_management/print_poshe_nokhodi.html', cx)


class exel_yegaan_khedmat(View):
    def get(self, request):
        form = FormYegankhedmati()
        form.fields['type'].choices = [(1, 'عادی'), (2, "امریه")]
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_yegann_khedmati.html', cx)

    def post(self, request):
        form = FormYegankhedmati(request.POST, request.FILES or None)
        form.fields['type'].choices = [(1, 'عادی'), (2, "امریه")]
        if not form.is_valid():
            cx = {'form': form}
            return render(request, 'ensani_soldires_management/update_yegann_khedmati.html', cx)
        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c",
                                                                                                              " ")
                    one_soldire_list.append(cell_value)
                if one_soldire_list[0] is not None:
                    print(form.cleaned_data['type'])
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if form.cleaned_data['type'] == "1":
                        if find_soldire is not None:
                            for iteam in list_yegan_bekargirande:
                                if iteam[1] == one_soldire_list[1]:
                                    find_soldire.unit_name = iteam[1]
                                    find_soldire.unit_type = iteam[2]
                                find_soldire.save()
                    if form.cleaned_data['type'] == "2":
                        if find_soldire is not None:
                            find_soldire.Amriye = True
                            find_soldire.Amriye_organization = one_soldire_list[1]
                            find_soldire.save()
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_yegann_khedmati.html', cx)


def export_soldire_incoures_all_data(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'name', 'family', 'fathers_name', 'National_Code', 'acceptance_code', 't_Gordan__name',
        't_battalion_group__name', 'code_gorhan_nahai', 'Amriye', 'Amriye_organization', 'physical_condition',
        'Type_of_disease', 'Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
        'marital_status', 'Religion', 'Date_of_birth', 'place_of_birth', 'phone_number', 'home_phone_number',
        'Date_of_dispatch', 'province_name', 'city_name', 'Address', 'Place_of_Issue', 'height', 'Weight',
        'Renewal_of_the_previous_period', 'attraction_of_the_organization', 'unit_name', 'unit_type').order_by(
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عدد پذیرش',
        't_Gordan__name': 'نام گردان جدید',
        't_battalion_group__name': 'نام گروهان جدید',
        'code_gorhan_nahai': 'کد گروهان جدید',
        'Amriye': 'امریه دار',
        'Amriye_organization': 'سازمان امریه',
        'physical_condition': 'وضعیت جسمانی',
        'Type_of_disease': 'نوع بیماری',
        'Grade': 'مقطع تحصیلی',
        'Grade_precise': 'مقطع تحصیلی دقیق',
        'educational_level_of_the_system': 'مقطع تحصیلی سامانه',
        'Study_group': 'گروه تحصیلی',
        'marital_status': 'وضعیت تاهل',
        'Religion': 'مذهب',
        'Date_of_birth': 'تاریخ تولد',
        'place_of_birth': 'محل تولد',
        'phone_number': 'شماره موبایل',
        'home_phone_number': 'شماره منزل',
        'Date_of_dispatch': 'تاریخ اعزام',
        'province_name': 'نام استان',
        'city_name': 'نام شهر',
        'Address': 'آدرس',
        'Place_of_Issue': 'محل صدور',
        'height': 'قد',
        'Weight': 'وزن',
        'Renewal_of_the_previous_period': 'جدید دوره قبل',
        'attraction_of_the_organization': 'جذبی',
        'unit_name': 'نام یگان بکارگیرنده',
        'unit_type': 'نوع یگان بکارگیرنده',
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_all_soldire_in_course.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


def export_soldire_Sufficiency_of_mobilization_all_data(request):
    queryset = Soldier.objects.filter(has_been_accepted=True,
                                      Sufficiency_of_mobilization=True).values(
        'name', 'family', 'fathers_name', 'National_Code', 'acceptance_code', 'Amriye', 'Amriye_organization',
        'physical_condition',
        'Type_of_disease', 'Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
        'marital_status', 'Religion', 'Date_of_birth', 'place_of_birth', 'phone_number', 'home_phone_number',
        'Date_of_dispatch', 'province_name', 'city_name', 'Address', 'Place_of_Issue', 'height', 'Weight',
        'Renewal_of_the_previous_period', 'attraction_of_the_organization', 'unit_name', 'unit_type').order_by(
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عدد پذیرش',
        'Amriye': 'امریه دار',
        'Amriye_organization': 'سازمان امریه',
        'physical_condition': 'وضعیت جسمانی',
        'Type_of_disease': 'نوع بیماری',
        'Grade': 'مقطع تحصیلی',
        'Grade_precise': 'مقطع تحصیلی دقیق',
        'educational_level_of_the_system': 'مقطع تحصیلی سامانه',
        'Study_group': 'گروه تحصیلی',
        'marital_status': 'وضعیت تاهل',
        'Religion': 'مذهب',
        'Date_of_birth': 'تاریخ تولد',
        'place_of_birth': 'محل تولد',
        'phone_number': 'شماره موبایل',
        'home_phone_number': 'شماره منزل',
        'Date_of_dispatch': 'تاریخ اعزام',
        'province_name': 'نام استان',
        'city_name': 'نام شهر',
        'Address': 'آدرس',
        'Place_of_Issue': 'محل صدور',
        'height': 'قد',
        'Weight': 'وزن',
        'Renewal_of_the_previous_period': 'جدید دوره قبل',
        'attraction_of_the_organization': 'جذبی',
        'unit_name': 'نام یگان بکارگیرنده',
        'unit_type': 'نوع یگان بکارگیرنده',
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_soldire_Sufficiency_of_mobilization_all_data.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


def export_soldire_Previous_service_record_all_data(request):
    queryset = Soldier.objects.filter(has_been_accepted=True,
                                      Previous_service_record=True).values(
        'name', 'family', 'fathers_name', 'National_Code', 'acceptance_code', 'Amriye', 'Amriye_organization',
        'physical_condition',
        'Type_of_disease', 'Grade', 'Grade_precise', 'educational_level_of_the_system', 'Study_group',
        'marital_status', 'Religion', 'Date_of_birth', 'place_of_birth', 'phone_number', 'home_phone_number',
        'Date_of_dispatch', 'province_name', 'city_name', 'Address', 'Place_of_Issue', 'height', 'Weight',
        'Renewal_of_the_previous_period', 'attraction_of_the_organization', 'unit_name', 'unit_type').order_by(
        't_Gordan__name', 't_battalion_group__name', 'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عدد پذیرش',
        'Amriye': 'امریه دار',
        'Amriye_organization': 'سازمان امریه',
        'physical_condition': 'وضعیت جسمانی',
        'Type_of_disease': 'نوع بیماری',
        'Grade': 'مقطع تحصیلی',
        'Grade_precise': 'مقطع تحصیلی دقیق',
        'educational_level_of_the_system': 'مقطع تحصیلی سامانه',
        'Study_group': 'گروه تحصیلی',
        'marital_status': 'وضعیت تاهل',
        'Religion': 'مذهب',
        'Date_of_birth': 'تاریخ تولد',
        'place_of_birth': 'محل تولد',
        'phone_number': 'شماره موبایل',
        'home_phone_number': 'شماره منزل',
        'Date_of_dispatch': 'تاریخ اعزام',
        'province_name': 'نام استان',
        'city_name': 'نام شهر',
        'Address': 'آدرس',
        'Place_of_Issue': 'محل صدور',
        'height': 'قد',
        'Weight': 'وزن',
        'Renewal_of_the_previous_period': 'جدید دوره قبل',
        'attraction_of_the_organization': 'جذبی',
        'unit_name': 'نام یگان بکارگیرنده',
        'unit_type': 'نوع یگان بکارگیرنده',
    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=list_soldire_Sufficiency_of_mobilization_all_data.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MyModelData')

        # دسترسی به workbook و sheet برای تغییر جهت به راست به چپ
        workbook = writer.book
        worksheet = writer.sheets['MyModelData']

        # تنظیم sheet به حالت راست به چپ
        worksheet.sheet_view.rightToLeft = True

    # تنظیم sheet به حالت راست به چپ
    worksheet.sheet_view.rightToLeft = True
    return response


class update_db_from_exel_all_soldire_in_course(View):
    def get(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse()
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_db_from_exel_all_soldire_in_course.html', cx)

    def post(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request, 'ensani_soldires_management/update_db_from_exel_all_soldire_in_course.html', cx)
        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c",
                                                                                                              " ")
                    one_soldire_list.append(cell_value)
                if one_soldire_list[3] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[3]).first()
                    find_soldire.name = one_soldire_list[0]
                    find_soldire.family = one_soldire_list[1]
                    find_soldire.fathers_name = one_soldire_list[2]
                    find_soldire.acceptance_code = one_soldire_list[3]
                    if one_soldire_list[4] is not None:
                        gordan = battalion.objects.filter(name__icontains=one_soldire_list[4]).first()
                        find_soldire.t_Gordan = gordan
                        if one_soldire_list[5] is not None:
                            gorhan = battalion_group.objects.filter(name__icontains=one_soldire_list[5],
                                                                    gordan=gordan).first()
                            find_soldire.t_battalion_group = gorhan
                        if one_soldire_list[6] is not None:
                            find_soldire.code_gorhan_nahai = int(one_soldire_list[6])
                    find_soldire.Amriye = one_soldire_list[7]
                    find_soldire.Amriye_organization = one_soldire_list[8]
                    find_soldire.physical_condition = one_soldire_list[9]
                    find_soldire.Type_of_disease = one_soldire_list[10]
                    find_soldire.Grade = one_soldire_list[11]
                    find_soldire.Grade_precise = one_soldire_list[12]
                    find_soldire.educational_level_of_the_system = one_soldire_list[13]
                    find_soldire.Study_group = one_soldire_list[14]
                    find_soldire.marital_status = one_soldire_list[15]
                    find_soldire.Religion = one_soldire_list[16]
                    find_soldire.Date_of_birth = one_soldire_list[17]
                    find_soldire.Date_of_dispatch = one_soldire_list[18]
                    find_soldire.phone_number = one_soldire_list[19]
                    find_soldire.home_phone_number = one_soldire_list[20]
                    find_soldire.Date_of_dispatch = one_soldire_list[21]
                    find_soldire.province_name = one_soldire_list[22]
                    find_soldire.city_name = one_soldire_list[23]
                    find_soldire.Address = one_soldire_list[24]
                    find_soldire.Place_of_Issue = one_soldire_list[25]
                    find_soldire.height = one_soldire_list[26]
                    find_soldire.Weight = one_soldire_list[27]
                    find_soldire.Renewal_of_the_previous_period = one_soldire_list[28]
                    find_soldire.attraction_of_the_organization = one_soldire_list[29]
                    find_soldire.unit_name = one_soldire_list[30]
                    find_soldire.unit_type = one_soldire_list[31]
                    find_soldire.save()
        cx = {'form': form}
        return render(request, 'ensani_soldires_management/update_yegann_khedmati.html', cx)


class update_db_from_exel_all_soldire_Previous_service_record(View):
    def get(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/update_db_from_exel_all_soldire_Previous_service_record.html', cx)

    def post(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'ensani_soldires_management/update_db_from_exel_all_soldire_Previous_service_record.html', cx)
        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c",
                                                                                                              " ")
                    one_soldire_list.append(cell_value)
                if one_soldire_list[3] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[3]).first()
                    find_soldire.name = one_soldire_list[0]
                    find_soldire.family = one_soldire_list[1]
                    find_soldire.fathers_name = one_soldire_list[2]
                    find_soldire.acceptance_code = one_soldire_list[4]
                    find_soldire.Amriye = one_soldire_list[5]
                    find_soldire.Amriye_organization = one_soldire_list[6]
                    find_soldire.physical_condition = one_soldire_list[7]
                    find_soldire.Type_of_disease = one_soldire_list[8]
                    find_soldire.Grade = one_soldire_list[9]
                    find_soldire.educational_level_of_the_system = one_soldire_list[10]
                    find_soldire.Grade = one_soldire_list[11]
                    find_soldire.Study_group = one_soldire_list[12]
                    find_soldire.marital_status = one_soldire_list[13]
                    find_soldire.Religion = one_soldire_list[14]
                    find_soldire.Date_of_birth = one_soldire_list[15]
                    find_soldire.place_of_birth = one_soldire_list[16]
                    find_soldire.phone_number = one_soldire_list[17]
                    find_soldire.home_phone_number = one_soldire_list[18]
                    find_soldire.Date_of_dispatch = one_soldire_list[19]
                    find_soldire.province_name = one_soldire_list[20]
                    find_soldire.city_name = one_soldire_list[21]
                    find_soldire.Address = one_soldire_list[22]
                    find_soldire.Date_of_dispatch = one_soldire_list[23]
                    find_soldire.height = one_soldire_list[24]
                    find_soldire.Weight = one_soldire_list[25]
                    find_soldire.Renewal_of_the_previous_period = one_soldire_list[26]
                    find_soldire.attraction_of_the_organization = one_soldire_list[27]
                    find_soldire.unit_name = one_soldire_list[28]
                    find_soldire.unit_type = one_soldire_list[29]
                    find_soldire.save()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/update_db_from_exel_all_soldire_Previous_service_record.html', cx)


class update_db_from_exel_all_soldire_Sufficiency_of_mobilization(View):
    def get(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/update_db_from_exel_all_soldire_Sufficiency_of_mobilization.html', cx)

    def post(self, request):
        form = FormUpdateAllSoldiresHasbenAceptedInCourse(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'ensani_soldires_management/update_db_from_exel_all_soldire_Sufficiency_of_mobilization.html',
                          cx)

        else:
            exel = request.FILES['file']

            workbook = openpyxl.load_workbook(exel)

            # انتخاب شیت اول
            sheet = workbook.active

            # بدست آوردن تعداد ردیف‌ها و ستون‌ها
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            # برای هر ردیف از ردیف دوم به بعد (برای نادیده‌گرفتن هدر)
            for row_idx in range(2, num_rows + 1):
                one_soldire_list = []
                for col_idx in range(1, num_cols + 1):
                    # مقدار سلول را بخوانید
                    cell_value = sheet.cell(row=row_idx, column=col_idx).value
                    if cell_value is not None:
                        # جایگزینی کاراکترهای عربی با کاراکترهای فارسی
                        cell_value = str(cell_value)
                        cell_value = cell_value.replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace("\u200c",
                                                                                                              " ")
                    one_soldire_list.append(cell_value)
                if one_soldire_list[3] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[3]).first()
                    find_soldire.name = one_soldire_list[0]
                    find_soldire.family = one_soldire_list[1]
                    find_soldire.fathers_name = one_soldire_list[2]
                    find_soldire.acceptance_code = one_soldire_list[4]
                    find_soldire.Amriye = one_soldire_list[5]
                    find_soldire.Amriye_organization = one_soldire_list[6]
                    find_soldire.physical_condition = one_soldire_list[7]
                    find_soldire.Type_of_disease = one_soldire_list[8]
                    find_soldire.Grade = one_soldire_list[9]
                    find_soldire.educational_level_of_the_system = one_soldire_list[10]
                    find_soldire.Grade = one_soldire_list[11]
                    find_soldire.Study_group = one_soldire_list[12]
                    find_soldire.marital_status = one_soldire_list[13]
                    find_soldire.Religion = one_soldire_list[14]
                    find_soldire.Date_of_birth = one_soldire_list[15]
                    find_soldire.place_of_birth = one_soldire_list[16]
                    find_soldire.phone_number = one_soldire_list[17]
                    find_soldire.home_phone_number = one_soldire_list[18]
                    find_soldire.Date_of_dispatch = one_soldire_list[19]
                    find_soldire.province_name = one_soldire_list[20]
                    find_soldire.city_name = one_soldire_list[21]
                    find_soldire.Address = one_soldire_list[22]
                    find_soldire.Date_of_dispatch = one_soldire_list[23]
                    find_soldire.height = one_soldire_list[24]
                    find_soldire.Weight = one_soldire_list[25]
                    find_soldire.Renewal_of_the_previous_period = one_soldire_list[26]
                    find_soldire.attraction_of_the_organization = one_soldire_list[27]
                    find_soldire.unit_name = one_soldire_list[28]
                    find_soldire.unit_type = one_soldire_list[29]
                    find_soldire.save()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/update_db_from_exel_all_soldire_Sufficiency_of_mobilization.html', cx)
