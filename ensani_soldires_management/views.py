import jdatetime
from django.shortcuts import render
from django.views import View

from ensani_soldires_management.forms import FormUpdateGordan, Formjazbi, FormYegankhedmati, \
    FormUpdateAllSoldiresHasbenAceptedInCourse, FormUpdateAllSoldires, FormRankGroup
from soldiers.forms import FormUpdateRank, FormUpdateBank
from soldiers.models import Soldier
from ensani_letter.models import NormalLetterModels
import pandas as pd
from django.http import HttpResponse, JsonResponse
import openpyxl
from battalions.models import battalion, battalion_group
from ensaniapp_settings.models import EnsaniSettings

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
    (116, 'بیمارستان  شهید صدوقی نزسا', 'نزسا', '******', '******'),
    (117, 'ستاد سپاه قائم آل محمد (عج) - سمنان', 'سپاه و رده های اقماری', '******', '******'),
    (118, 'مرکز جنگال فلق نزسا', 'نزسا', '******', '******'),
    (119, 'مرکز 23 نبوت نزسا', 'نزسا', '******', '******'),
    (120, 'مرکز پشتيباني عمومي و تخصصي (جنوب شرق)', 'نزسا', '******', '******'),
    (121, 'دانشگاه علوم پزشکي بقيه‌ا... ‌الاعظم (عج)', 'سپاه و رده های اقماری', 'تهران',
     'تهران- میدان ونک ابتدای خیابان ملاصدرا'),
    (122, 'پايگاه پهپاد نبي اکرم (ص) نزسا', 'نزسا', '******', '******'),
    (123, 'فرماندهي قرارگاه پشتيباني ستاد کل سپاه', 'سپاه و رده های اقماری', '******', '******'),
    (124, 'فرماندهي هوانيروز - پايگاه بالگردي رزمي جنوب‌شرق نزسا', 'نزسا', '******', '******'),
    (125, 'قرارگاه فرهنگي اجتماعي شهيد برونسي', 'سپاه و رده های اقماری', '******', '******'),
    (126, 'فرماندهي سايبرالکترونيک سپاه', 'سپاه و رده های اقماری', '******', '******'),
    (127, ' قرارگاه فرهنگي بقيه ا... الاعظم عج', 'سپاه و رده های اقماری', '******', '******'),
    (128, 'گروه 43 مهندسي امام علي(ع) نزسا', 'نزسا', '******', '******'),
    (129, 'فرماندهي حفاظت، امنيت سپاه', 'سپاه و رده های اقماری', '******', '******'),
    (130, 'دانشگاه حضرت اميرالمومنين(ع) نزسا', 'نزسا', '******', '******'),
    (131, 'سپاه روح اله - مرکزي', 'سپاه و رده های اقماری', '******', '******'),
    (132, 'سپاه انصارالحسين (ع) - همدان', 'سپاه و رده های اقماری', '******', '******'),

]


# Create your views here.
def all_soldire(request):
    soldires = Soldier.objects.filter(has_been_accepted=True, in_coures=True)
    context = {
        'results': soldires
    }

    return render(request, 'ensani_soldires_management/all_soldires.html', context)


def soldier_search(request):
    query = request.GET.get('name')
    family = request.GET.get('family')
    national_code = request.GET.get('national_code')
    physical_condition = request.GET.get('physical_condition')
    marital_status = request.GET.get('marital_status')
    religion = request.GET.get('religion')
    acceptance_code = request.GET.get('acceptance_code')
    Grade = request.GET.get('Grade')
    Grade_precise = request.GET.get('Grade_precise')
    Gordan = request.GET.get('Gordan')
    amire = request.GET.get('amire')
    battaliongroup = request.GET.get('battalion_group')
    soldiers = Soldier.objects.all()
    gordan = battalion.objects.filter().all()
    grohan = battalion_group.objects.filter().all()
    count_f = soldiers
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
    if Grade:
        soldiers = soldiers.filter(Grade=Grade)
    if Grade_precise:
        soldiers = soldiers.filter(Grade_precise=Grade_precise)

    if Gordan:
        soldiers = soldiers.filter(Gordan__name__icontains=Gordan)

    if battaliongroup:
        soldiers = soldiers.filter(battalion_group__name__icontains=battaliongroup)

    if amire:
        soldiers = soldiers.filter(Amriye=amire)

    op_result = False
    count_e = soldiers
    if count_f != count_e:
        op_result = True

    context = {
        'results': soldiers, 'op_result': op_result, 'gordan': gordan, 'grohan': grohan,
    }

    return render(request, 'ensani_soldires_management/soldier_search.html', context)


def get_grohan_by_gordan_for_search(request):
    gordan_name = request.GET.get('gordan_name')
    grohan_list = battalion_group.objects.filter(gordan__name__icontains=gordan_name).values('id', 'name')
    return JsonResponse(list(grohan_list), safe=False)


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
                    print(one_soldire_list)
                if one_soldire_list[0] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if find_soldire is not None:
                        t_gordan = battalion.objects.filter(name__icontains=one_soldire_list[5]).first()
                        t_gorohan = battalion_group.objects.filter(gordan=t_gordan,
                                                                   name__icontains=one_soldire_list[6]).first()
                        find_soldire.t_Gordan = t_gordan
                        find_soldire.t_battalion_group = t_gorohan
                        code_nahai_gorohan = one_soldire_list[7]
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
        't_Gordan__name', 't_battalion_group__name')

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
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if form.cleaned_data['type'] == "1":
                        if find_soldire is not None:
                            for iteam in list_yegan_bekargirande:
                                if iteam[1].replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace(
                                        "\u200c",
                                        " ") == one_soldire_list[1]:
                                    find_soldire.unit_name = iteam[1]
                                    find_soldire.unit_type = iteam[2]
                                    find_soldire.unit_province = iteam[3]
                                    find_soldire.unit_address = iteam[4]
                                    find_soldire.IsUnit = True
                                    find_soldire.save()
                                    break
                    if form.cleaned_data['type'] == "2":
                        if find_soldire is not None:
                            for iteam in list_yegan_bekargirande:
                                if iteam[1].replace('ي', 'ی').replace('ك', 'ک').replace('ؤ', 'و').replace(
                                        "\u200c",
                                        " ") == one_soldire_list[1]:
                                    find_soldire.unit_name = iteam[1]
                                    find_soldire.unit_type = iteam[2]
                                    find_soldire.unit_province = iteam[3]
                                    find_soldire.unit_address = iteam[4]
                                    find_soldire.IsUnit = True
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
                    find_soldire.acceptance_code = one_soldire_list[4]
                    if one_soldire_list[5] is not None:
                        gordan = battalion.objects.filter(name__icontains=one_soldire_list[5]).first()
                        find_soldire.t_Gordan = gordan
                        if one_soldire_list[6] is not None:
                            gorhan = battalion_group.objects.filter(name__icontains=one_soldire_list[6],
                                                                    gordan=gordan).first()
                            find_soldire.t_battalion_group = gorhan
                        if one_soldire_list[7] is not None:
                            find_soldire.code_gorhan_nahai = int(one_soldire_list[7])
                    find_soldire.Amriye = one_soldire_list[8]
                    find_soldire.Amriye_organization = one_soldire_list[9]
                    find_soldire.physical_condition = one_soldire_list[10]
                    find_soldire.Type_of_disease = one_soldire_list[11]
                    find_soldire.Grade = one_soldire_list[12]
                    find_soldire.Grade_precise = one_soldire_list[13]
                    find_soldire.educational_level_of_the_system = one_soldire_list[14]
                    find_soldire.Study_group = one_soldire_list[15]
                    find_soldire.marital_status = one_soldire_list[16]
                    find_soldire.Religion = one_soldire_list[17]
                    find_soldire.Date_of_birth = one_soldire_list[18]
                    find_soldire.Date_of_dispatch = one_soldire_list[19]
                    find_soldire.phone_number = one_soldire_list[20]
                    find_soldire.home_phone_number = one_soldire_list[21]
                    find_soldire.Date_of_dispatch = one_soldire_list[22]
                    find_soldire.province_name = one_soldire_list[23]
                    find_soldire.city_name = one_soldire_list[24]
                    find_soldire.Address = one_soldire_list[25]
                    find_soldire.Place_of_Issue = one_soldire_list[26]
                    find_soldire.height = one_soldire_list[27]
                    find_soldire.Weight = one_soldire_list[28]
                    find_soldire.Renewal_of_the_previous_period = one_soldire_list[29]
                    find_soldire.attraction_of_the_organization = one_soldire_list[30]
                    find_soldire.unit_name = one_soldire_list[31]
                    find_soldire.unit_type = one_soldire_list[32]
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


def import_and_export_excel_maharat(request):
    # خواندن فایل اکسل ورودی که حاوی کد ملی‌ها است
    input_file_path = "D:/unittest/ensaniapp/soldiers/xxx.xlsx"  # مسیر فایل اکسل ورودی
    national_codes_df = pd.read_excel(input_file_path)

    # اطمینان از اینکه ستون کد ملی به درستی خوانده شده است
    national_codes = national_codes_df['National_Code'].tolist()

    # واکشی اطلاعات سربازان براساس کد ملی‌ها
    soldiers_data = []
    for code in national_codes:
        soldier = Soldier.objects.filter(
            National_Code__icontains=code  # جستجوی تقریبی بر اساس کد ملی
        ).values('National_Code', 'Date_of_birth', 'Address', 'home_phone_number', 'phone_number', 'Grade', 'Address',
                 'name', 'family', 'fathers_name').first()

        # افزودن به لیست نتایج در صورت یافتن
        if soldier:
            soldiers_data.append(soldier)
    # تبدیل داده‌ها به DataFrame با استفاده از pandas
    df = pd.DataFrame(soldiers_data)

    # ایجاد پاسخ HTTP برای دانلود فایل اکسل
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=soldiers_filtered_data.xlsx'

    # ذخیره داده‌ها در قالب اکسل
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Filtered Soldiers Data')

    return response


import io
import zipfile
from django.http import HttpResponse


def import_and_export_multiple_excel_sakhtar_sazi(request):
    # ایجاد فایل فشرده در حافظه
    zip_buffer = io.BytesIO()

    # باز کردن فایل فشرده برای نوشتن فایل‌ها
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # مجموعه‌های مختلف داده‌ها برای ایجاد فایل‌های مختلف اکسل
        data_sets = {}

        bn = battalion.objects.all()
        for b in bn:
            for bg in battalion_group.objects.filter(gordan=b):
                # تعریف مجموعه داده برای هر گروهان
                soldiers_filtered_data = Soldier.objects.filter(
                    t_battalion_group=bg,
                    t_Gordan=b,
                    willing_to_learn=True,
                    in_coures=True
                ).order_by('code_gorhan_nahai').values(
                    'National_Code', 'code_gorhan_nahai'
                )

                # اضافه کردن مجموعه داده به دیکشنری
                data_sets[f"{b.name}_{bg.name}"] = soldiers_filtered_data

        # ایجاد هر فایل اکسل و اضافه کردن به فایل ZIP
        for file_name, queryset in data_sets.items():
            # تبدیل queryset به DataFrame
            df = pd.DataFrame(list(queryset))

            if not df.empty:  # بررسی خالی نبودن مجموعه داده
                # تغییر نام ستون‌ها
                df.rename(columns={
                    'National_Code': 'کد ملی',
                    'code_gorhan_nahai': 'کد سازمانی'
                }, inplace=True)

                excel_buffer = io.BytesIO()
                # نوشتن DataFrame در فایل اکسل
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)

                # افزودن فایل اکسل به فایل فشرده
                zf.writestr(f'{file_name}.xlsx', excel_buffer.getvalue())

    # آماده‌سازی فایل ZIP برای دانلود
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="sakhtar_sazi.zip"'
    return response


def export_to_excel_list_not_accepted(request):
    queryset = Soldier.objects.filter(has_been_accepted=False, date_improt_type='سامانه').values(
        'name', 'family', 'fathers_name',
        'National_Code', 'phone_number', 'home_phone_number')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'phone_number': 'موبایل',
        'home_phone_number': 'منزل',

    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export_to_excel_list_not_accepted.xlsx'

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


def get_military_rank(education, score):
    # تعریف جدول درجات و محدوده نمرات
    rank_table = {
        "دکتری": {
            "ستوان یکم": (0, 20),
        },
        "فوق لیسانس": {
            "ستوان یکم": (10, 20),
            "ستوان دوم": (6, 9.9),
            "ستوان سوم": (0, 5.9),
        },
        "لیسانس": {
            "ستوان دوم": (10, 20),
            "ستوان سوم": (7, 9.9),
            "رزمدار یکم": (6, 6.9),
            "رزمدار دوم": (4, 5.9),
            "رزم‌آور یکم": (2, 3.9),
            "رزم‌آور دوم": (0, 1.9),
        },
        "فوق دیپلم": {
            "رزم‌آور یکم": (5, 20),
            "رزم‌آور دوم": (2, 4.9),
            "رزم‌آور سوم": (0, 1.9),
        },
        "دیپلم": {
            "رزمیار": (5, 20),
            "سرباز یکم": (2, 4.9),
            "سرباز دوم": (0, 1.9),
        },
        "زیر دیپلم": {
            "سرباز دوم": (2, 20),
            "سرباز": (0, 1.9),
        },
    }

    # بررسی وجود مدرک تحصیلی در جدول
    if education not in rank_table:
        return "مدرک تحصیلی نامعتبر است."

    # جستجو در جدول برای پیدا کردن درجه مناسب
    for rank, (min_score, max_score) in rank_table[education].items():
        if min_score <= score <= max_score:
            return rank

    return "نمره در محدوده تعریف‌شده نیست."


def calculate_score():
    soldire = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).all()
    mapping_discipline_score = {
        13: 0.5,
        14: 0.5,
        15: 1,
        16: 1,
        17: 1.5,
        18: 1.5,
        19: 2,
        20: 2
    }
    mapping_battalion_activity = {
        16: 0.5,
        17: 1,
        18: 1.5,
        19: 2,
        20: 2.5,
    }
    mapping_battalion_sample = {
        True: 2
    }

    # بسیج(4 نمره)
    mapping_basij_efficiency = {
        '30 روزه': 0.5,
        '45 روزه': 1,
    }

    # حوزه(1 نمره)
    mapping_ideological_score = {
        18: 0.4,
        19: 0.7,
        20: 1
    }
    mapping_top_three = {
        'نفر اول': 2,
        'نفر دوم': 1.5,
        'نفر سوم': 1,
    }
    mapping_shooting_score = {}
    for i in range(80, 85):
        mapping_shooting_score[i] = 0.4

    for i in range(84, 90):
        mapping_shooting_score[i] = 0.7

    for i in range(90, 96):
        mapping_shooting_score[i] = 1.5

    for i in range(95, 101):
        mapping_shooting_score[i] = 2
    # اطلاعات مربوط به فراگیر(6.5 نمره)
    mapping_nahj_memorization = {
        True: 1
    }
    mapping_sajjadiya_memorization = {
        True: 1
    }
    mapping_global_awards = {
        1: 0.3,
        2: 0.4,
    }
    mapping_national_awards = {
        1: 0.2,
        2: 0.3,
    }
    mapping_provincial_awards = {
        1: 0.1,
        2: 0.2,
    }
    mapping_global_articles = {
        1: 0.2,
        2: 0.3,
    }
    mapping_publications = {
        1: 0.2,
        2: 0.3,
    }

    for s in soldire:
        total = 0
        # محاسبه گردان
        discipline_score = s.discipline_score  # انضباط (2 نمره)
        battalion_activity = s.battalion_activity  # فعالیت در گردان (2.5 نمره)
        battalion_sample = s.battalion_sample  # نمونه گردان (2 نمره مازاد)
        total += mapping_discipline_score.get(int(discipline_score), 0)
        total += mapping_battalion_activity.get(int(battalion_activity), 0)
        total += mapping_battalion_sample.get(battalion_sample, 0)
        # بسیح
        basij_experience = int(s.basij_experience) * 0.0142857  # 0.0142857 سابقه بسیج فعال به ماه (2 نمره)
        council_experience = int(s.council_experience) * 0.01  # سابقه عضو شورای پایگاه به ماه (1 نمره)0.01
        basij_efficiency = s.basij_efficiency
        total += basij_experience
        total += council_experience
        total += mapping_basij_efficiency.get(str(basij_efficiency), 0)
        # عقیدتی
        ideological_score = s.ideological_score  # نمره عقیدتی (1 نمره)
        total += mapping_ideological_score.get(int(ideological_score), 0)
        # آموزش
        shooting_score = int(s.shooting_score)  # نمره میدان تیر (2 نمره)
        top_three = s.top_three  # سه نفر برتر (2 نمره)
        total += mapping_shooting_score.get(shooting_score, 0)
        total += mapping_top_three.get(top_three, 0)
        # اطلاعات مربوط به فراگیر
        quran_memorization = s.quran_memorization * 0.1  # حافظ قرآن (جزء) (3 نمره)
        nahj_memorization = s.nahj_memorization  # حافظ نهج البلاغه (1 نمره)
        sajjadiya_memorization = s.sajjadiya_memorization  # حافظ صحیفه سجادیه (1 نمره)
        global_awards = s.global_awards  # تعداد مقام جهانی
        national_awards = s.national_awards  # تعداد مقام کشوری
        provincial_awards = s.provincial_awards  # تعداد مقام استانی
        global_articles = s.global_articles  # تعداد مقالات جهانی
        publications = s.publications  # تعداد تالیفات
        total += quran_memorization
        total += mapping_nahj_memorization.get(nahj_memorization, 0)
        total += mapping_sajjadiya_memorization.get(sajjadiya_memorization, 0)
        if global_awards > 0 and global_awards < 3:
            total += mapping_global_awards.get(global_awards, 0)
        elif global_awards < 0:
            total += mapping_global_awards.get(0, 0)
        elif global_awards > 3:
            total += 0.4

        if national_awards > 0 and national_awards < 3:
            total += mapping_national_awards.get(national_awards, 0)
        elif national_awards < 0:
            total += mapping_national_awards.get(0, 0)
        elif national_awards > 3:
            total += 0.3

        if provincial_awards > 0 and provincial_awards < 3:
            total += mapping_provincial_awards.get(provincial_awards, 0)
        elif provincial_awards < 0:
            total += mapping_provincial_awards.get(0, 0)
        elif provincial_awards > 3:
            total += 0.2

        if global_articles > 0 and global_articles < 3:
            total += mapping_global_articles.get(global_articles, 0)
        elif global_articles < 0:
            total += mapping_global_articles.get(0, 0)
        elif global_articles > 3:
            total += 0.3

        if publications > 0 and publications < 3:
            total += mapping_publications.get(publications, 0)
        elif publications < 0:
            total += mapping_publications.get(0, 0)
        elif publications > 3:
            total += 0.3

        if total > 20:
            total = 20
        rank = ''
        if s.Amriye == True or s.physical_condition != 'سالم':
            rank = get_military_rank(s.Grade, 0)
        else:
            rank = get_military_rank(s.Grade, total)
        s.rank = rank
        s.total_score = total
        s.save()


class import_rank_from_exel(View):
    def get(self, request):
        form = FormUpdateRank()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/import_rank_from_exel.html', cx)

    def post(self, request):
        form = FormUpdateRank(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'ensani_soldires_management/import_rank_from_exel.html',
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
                    one_soldire_list.append(cell_value)
                if one_soldire_list[0] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    find_soldire.discipline_score = one_soldire_list[6]
                    find_soldire.basij_experience = one_soldire_list[7]
                    find_soldire.council_experience = one_soldire_list[8]
                    find_soldire.ideological_score = one_soldire_list[9]
                    find_soldire.shooting_score = one_soldire_list[10]
                    find_soldire.global_awards = one_soldire_list[11]
                    find_soldire.national_awards = one_soldire_list[12]
                    find_soldire.provincial_awards = one_soldire_list[13]
                    find_soldire.global_articles = one_soldire_list[14]
                    find_soldire.publications = one_soldire_list[15]
                    find_soldire.battalion_activity = one_soldire_list[17]
                    find_soldire.battalion_sample = one_soldire_list[18] or False
                    find_soldire.basij_efficiency = one_soldire_list[19]
                    find_soldire.top_three = one_soldire_list[20]
                    find_soldire.quran_memorization = one_soldire_list[21] or 0
                    find_soldire.nahj_memorization = one_soldire_list[22] or False
                    find_soldire.sajjadiya_memorization = one_soldire_list[23] or False
                    find_soldire.save()
        cx = {'form': form}
        calculate_score()
        return render(request,
                      'ensani_soldires_management/import_rank_from_exel.html', cx)


def export_to_excel_list_bank(request):
    queryset = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).values(
        'name', 'family', 'fathers_name',
        'National_Code', 'acceptance_code', 't_Gordan', 't_battalion_group', 'code_gorhan_nahai',
        'bank_number').order_by('t_Gordan',
                                't_battalion_group',
                                'code_gorhan_nahai')

    df = pd.DataFrame(list(queryset))

    # تغییر نام ستون‌ها
    df.rename(columns={
        'name': 'نام',
        'family': 'نام خانوادگی',
        'fathers_name': 'نام پدر',
        'National_Code': 'کدملی',
        'acceptance_code': 'عددپذیرش',
        't_Gordan': 'گردان',
        't_battalion_group': 'گروهان',
        'code_gorhan_nahai': 'کدسازمانی',
        'bank_number': 'شماره حساب',

    }, inplace=True)
    # تنظیمات پاسخ HTTP برای اکسل

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export_to_excel_list_bank_number.xlsx'

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


class import_bank_number_from_exel(View):
    def get(self, request):
        form = FormUpdateBank()
        cx = {'form': form}
        return render(request,
                      'ensani_soldires_management/import_bank_from_exel.html', cx)

    def post(self, request):
        form = FormUpdateBank(request.POST, request.FILES or None)
        if not form.is_valid():
            cx = {'form': form}
            return render(request,
                          'ensani_soldires_management/import_bank_from_exel.html',
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
                    one_soldire_list.append(cell_value)
                if one_soldire_list[0] is not None:
                    find_soldire = Soldier.objects.filter(National_Code=one_soldire_list[0]).first()
                    if find_soldire is not None:
                        find_soldire.bank_number = one_soldire_list[1]
                        find_soldire.save()
        cx = {'form': form}
        calculate_score()
        return render(request,
                      'ensani_soldires_management/import_bank_from_exel.html', cx)


def rank_group_print(request):
    if request.method == "GET":
        form = FormRankGroup()

        context = {
            'form': form,
        }
        return render(request, 'ensani_soldires_management/rank_selector.html', context)
    if request.method == "POST":
        form = FormRankGroup(request.POST, request.FILES or None)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'ensani_soldires_management/rank_selector.html', context)
        start = int(form.cleaned_data['start']) + 1
        end = int(form.cleaned_data['end']) + 1

        sarbazha = Soldier.objects.filter(in_coures=True,
                                          has_been_accepted=True, willing_to_learn=True, acceptance_code__gte=start,
                                          acceptance_code__lt=end).order_by(
            'acceptance_code').all()
        en = EnsaniSettings.objects.filter().first()
        time = jdatetime.datetime.now()
        context = {
            'sarbazha': sarbazha,
            'en': en,
            'time': time,
        }
        return render(request, 'ensani_soldires_management/rank_print.html', context)


def rank_group_print_gordani(request):
    sarbazha = Soldier.objects.filter(in_coures=True,
                                      has_been_accepted=True, willing_to_learn=True,
                                      ).all().order_by(
        't_Gordan', 't_battalion_group', 'code_gorhan_nahai').all()
    en = EnsaniSettings.objects.filter().first()
    time = jdatetime.datetime.now()
    context = {
        'sarbazha': sarbazha,
        'en': en,
        'time': time,
    }
    return render(request, 'ensani_soldires_management/rank_print.html', context)
