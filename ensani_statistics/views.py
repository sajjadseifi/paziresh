from django.shortcuts import render
from soldiers.models import Soldier
from django.db.models import Count, Case, When
from battalions.models import battalion, battalion_group


# Create your views here.


def amar_avalie(request):
    statistics = []

    # ابتدا تمام گردان‌ها را بازیابی می‌کنیم
    battalions = battalion.objects.all()

    for bat in battalions:
        # دریافت همه گروهان‌های مربوط به این گردان
        groups = battalion_group.objects.filter(gordan=bat)
        total_soldiers = Soldier.objects.filter(Gordan=bat).all().count()
        battalion_name = bat.name
        lst = []
        salem = Soldier.objects.filter(Gordan=bat, physical_condition='سالم').all().count()
        moaf_az_razm = Soldier.objects.filter(Gordan=bat, physical_condition='معاف از رزم').all().count()
        goreh_b = Soldier.objects.filter(Gordan=bat, physical_condition='گروه ب').all().count()
        goreh_b_moaf_az_razm = Soldier.objects.filter(Gordan=bat, physical_condition='معاف+گروه ب').all().count()
        amire_dar = Soldier.objects.filter(Gordan=bat, Amriye=True).all().count()
        shie = Soldier.objects.filter(Gordan=bat, Religion='شیعه').all().count()
        ahle_tasanon = Soldier.objects.filter(Gordan=bat, Religion='اهل تسنن').all().count()
        for group in groups:
            # محاسبه تعداد سربازان برای هر گروهان
            soldiers = Soldier.objects.filter(battalion_group=group)
            lst.append((int(group.name), soldiers.count()))
        sorted_lst = sorted(lst, key=lambda x: x[0])

        remove_id_sorted_lst = []
        for iteam in sorted_lst:
            remove_id_sorted_lst.append(int(iteam[1]))
        sorted_lst = remove_id_sorted_lst
        statistics.append({
            'group_name': battalion_name,
            'total_soldiers': total_soldiers,
            'lst': sorted_lst,
            'salem': salem,
            'moaf_az_razm': moaf_az_razm,
            'goreh_b': goreh_b,
            'goreh_b_moaf_az_razm': goreh_b_moaf_az_razm,
            'amire_dar': amire_dar,
            'shie': shie,
            'ahle_tasanon': ahle_tasanon,

        })
        lst = []
    context = {
        'statistics': statistics
    }

    return render(request, 'ensani_statistics/vaziate_avalie.html', context)


def amar_gordan_gorhan(request):
    battalions = battalion.objects.all()
    stats = []

    for batt in battalions:
        groups = battalion_group.objects.filter(gordan=batt)
        group_stats_list = []
        zirediplom = 0
        diplom = 0
        lisans = 0
        ofghlisans = 0
        doctra = 0
        ofghdiplom = 0
        for group in groups:
            soldiers = Soldier.objects.filter(battalion_group=group)
            zirediplom += soldiers.filter(Grade="زیر دیپلم").all().count()
            diplom += soldiers.filter(Grade="دیپلم").all().count()
            ofghdiplom += soldiers.filter(Grade="فوق دیپلم").all().count()
            lisans += soldiers.filter(Grade="لیسانس").all().count()
            ofghlisans += soldiers.filter(Grade="فوق لیسانس").all().count()
            doctra += soldiers.filter(Grade="دکترا").all().count()
            degrees = soldiers.aggregate(
                zirediplom=Count(Case(When(Grade='زیر دیپلم', then=1))),
                diplom=Count(Case(When(Grade='دیپلم', then=1))),
                ofghdiplom=Count(Case(When(Grade='فوق دیپلم', then=1))),
                lisans=Count(Case(When(Grade='لیسانس', then=1))),
                ofghlisans=Count(Case(When(Grade='فوق لیسانس', then=1))),
                doctra=Count(Case(When(Grade='دکترا', then=1))),
            )
            group_stats = {
                'name': group.name,
                'degrees': degrees
            }
            group_stats_list.append(group_stats)

        battalion_stats = {
            'name': batt.name,
            'groups': group_stats_list,
            "zirediplom": zirediplom,
            "diplom": diplom,
            "lisans": lisans,
            "ofghlisans": ofghlisans,
            "doctra": doctra,
            "ofghdiplom": ofghdiplom,
            'count': (zirediplom + diplom + lisans + ofghlisans + doctra + ofghdiplom)
        }
        stats.append(battalion_stats)

    context = {
        'stats': stats
    }
    return render(request, 'ensani_statistics/amar_gordan_gorhan.html', context)


def amar_be_tafkik_madrk_tahsili(request):
    return render(request, 'ensani_statistics/amar_be_tafkik_madrak_tahsili.html')


def amar_shoro_doreh(request):
    return render(request, 'ensani_statistics/amar_shoro_doreh.html')


def amar_payan_dore(request):
    return render(request, 'ensani_statistics/amar_payan_dore.html')


def amar_avalie_samane(request):
    province_order = [
        'آذربایجان شرقی', 'آذربایجان غربی', 'اردبیل', 'اصفهان', 'البرز',
        'ایلام', 'بوشهر', 'تهران', 'چهارمحال و بختیاری', 'خراسان جنوبی',
        'خراسان رضوی', 'خراسان شمالی', 'خوزستان', 'زنجان', 'سمنان',
        'سیستان و بلوچستان', 'فارس', 'قزوین', 'قم', 'کردستان',
        'کرمان', 'کرمانشاه', 'کهگیلویه و بویراحمد', 'گلستان', 'گیلان',
        'لرستان', 'مازندران', 'مرکزی', 'همدان', 'یزد',
        'نامشخص'
    ]
    data = []

    for province in province_order:
        total = Soldier.objects.filter(province_name=province).count()
        salem = Soldier.objects.filter(province_name=province, physical_condition='سالم').count()
        moaf_az_razm = Soldier.objects.filter(province_name=province, physical_condition='معاف از رزم').count()
        goreh_b = Soldier.objects.filter(province_name=province, physical_condition='گروه ب').count()
        goreh_b_moaf_az_razm = Soldier.objects.filter(province_name=province, physical_condition='معاف+گروه ب').count()
        amire_dar = Soldier.objects.filter(province_name=province, Amriye=True).count()
        shie = Soldier.objects.filter(province_name=province, Religion='شیعه').count()
        ahle_tasanon = Soldier.objects.filter(province_name=province, Religion='اهل تسنن').count()
        zire_diplom = Soldier.objects.filter(province_name=province, Grade='زیر دیپلم').count()
        diplom = Soldier.objects.filter(province_name=province, Grade='دیپلم').count()
        fogh_diplom = Soldier.objects.filter(province_name=province, Grade='فوق دیپلم').count()
        lisans = Soldier.objects.filter(province_name=province, Grade='لیسانس').count()
        fogh_lisans = Soldier.objects.filter(province_name=province, Grade='فوق لیسانس').count()
        doctora = Soldier.objects.filter(province_name=province, Grade='دکتری').count()
        namoshakhas = total - (zire_diplom + diplom + fogh_diplom + lisans + fogh_lisans + doctora)

        data.append({
            'province': province,
            'total': total,
            'salem': salem,
            'moaf_az_razm': moaf_az_razm,
            'gorh_b': goreh_b,
            'goth_b_moaf_az_razm': goreh_b_moaf_az_razm,
            'shie': shie,
            'ahle_tasanon': ahle_tasanon,
            'amriye': amire_dar,
            'zire_diplom': zire_diplom,
            'diplom': diplom,
            'fogh_diplom': fogh_diplom,
            'lisans': lisans,
            'fogh_lisans': fogh_lisans,
            'doctora': doctora,
            'namoshakhas': namoshakhas,
        })
    soldire_total = Soldier.objects.filter(date_improt_type='سامانه').all().count()
    soldire_total_salem = Soldier.objects.filter(date_improt_type='سامانه', physical_condition='سالم').all().count()
    soldire_total_moafazrazm = Soldier.objects.filter(date_improt_type='سامانه',
                                                      physical_condition='معاف از رزم').all().count()
    soldire_total_shie = Soldier.objects.filter(date_improt_type='سامانه', Religion='شیعه').all().count()
    soldire_total_tasanon = Soldier.objects.filter(date_improt_type='سامانه', Religion='اهل تسنن').all().count()
    soldire_total_amire = Soldier.objects.filter(date_improt_type='سامانه', Amriye=True).all().count()
    zire_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='زیر دیپلم').count()
    diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='دیپلم').count()
    fogh_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق دیپلم').count()
    lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='لیسانس').count()
    fogh_lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق لیسانس').count()
    doctora = Soldier.objects.filter(date_improt_type='سامانه', Grade='دکتری').count()
    namoshakhas = Soldier.objects.filter(date_improt_type='سامانه', Grade='نامشخص').count()
    cx = {
        'data': data,
        'total': soldire_total,
        'soldire_total_salem': soldire_total_salem,
        'soldire_total_moafazrazm': soldire_total_moafazrazm,
        'soldire_total_shie': soldire_total_shie,
        'soldire_total_tasanon': soldire_total_tasanon,
        'soldire_total_amire': soldire_total_amire,
        'zire_diplom': zire_diplom,
        'diplom': diplom,
        'fogh_diplom': fogh_diplom,
        'lisans': lisans,
        'fogh_lisans': fogh_lisans,
        'doctora': doctora,
        'namoshakhas': namoshakhas

    }
    return render(request, 'ensani_statistics/amar_avlie_samane.html', cx)
