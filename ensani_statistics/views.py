from django.shortcuts import render, HttpResponse
from openpyxl.styles.builtins import total

import soldiers.import_data_from_exel
from soldiers.models import Soldier
from django.db.models import Count, Case, When
from battalions.models import battalion, battalion_group
from ensani_letter.models import NormalLetterModels
from ensaniapp_settings.models import EnsaniSettings
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def amar_avalie(request):
    settings = EnsaniSettings.objects.filter().first()
    if settings is None:
        return HttpResponse("تنظیمات دوره انجام نشده!")
    statistics = []
    total_soldire = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                           the_medical_commission=False, Sufficiency_of_mobilization=False).count()
    total_salme = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                         the_medical_commission=False, Sufficiency_of_mobilization=False,
                                         physical_condition='سالم').count()
    total_gorh_be = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                           the_medical_commission=False, Sufficiency_of_mobilization=False,
                                           physical_condition='گروه ب').count()
    total_moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                                the_medical_commission=False, Sufficiency_of_mobilization=False,
                                                physical_condition='معاف از رزم').count()
    total_moaf_az_razm_groh_be = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                                        the_medical_commission=False, Sufficiency_of_mobilization=False,
                                                        physical_condition='معاف+گروه ب').count()
    total_amrie_dar = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                             the_medical_commission=False, Sufficiency_of_mobilization=False,
                                             Amriye=True).count()
    total_shie = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                        the_medical_commission=False, Sufficiency_of_mobilization=False,
                                        Religion='شیعه').count()
    total_ahle_tasnon = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                               the_medical_commission=False, Sufficiency_of_mobilization=False,
                                               Religion='اهل تسنن').count()
    statistics = []
    if settings.tatbigh == False:

        # ابتدا تمام گردان‌ها را بازیابی می‌کنیم
        battalions = battalion.objects.all()
        for bat in battalions:
            # دریافت همه گروهان‌های مربوط به این گردان
            groups = battalion_group.objects.filter(gordan=bat)
            total_soldiers = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                                    the_medical_commission=False, Sufficiency_of_mobilization=False,
                                                    Previous_service_record=False, Gordan=bat).all().count()
            battalion_name = bat.name
            lst = []
            salem = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                           the_medical_commission=False, Sufficiency_of_mobilization=False,
                                           Previous_service_record=False,
                                           Gordan=bat, physical_condition='سالم').all().count()
            moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                                  the_medical_commission=False, Sufficiency_of_mobilization=False,
                                                  Previous_service_record=False,
                                                  Gordan=bat, physical_condition='معاف از رزم').all().count()
            goreh_b = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                             the_medical_commission=False, Sufficiency_of_mobilization=False,
                                             Previous_service_record=False,
                                             Gordan=bat, physical_condition='گروه ب').all().count()
            goreh_b_moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                          the_medical_commission=False,
                                                          Sufficiency_of_mobilization=False,
                                                          Previous_service_record=False,
                                                          in_coures=True, Gordan=bat,
                                                          physical_condition='معاف+گروه ب').all().count()
            amire_dar = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                               the_medical_commission=False, Sufficiency_of_mobilization=False,
                                               Previous_service_record=False,
                                               in_coures=True, Gordan=bat, Amriye=True).all().count()
            shie = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True, Gordan=bat,
                                          the_medical_commission=False, Sufficiency_of_mobilization=False,
                                          Previous_service_record=False,
                                          Religion='شیعه').all().count()
            ahle_tasanon = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                  the_medical_commission=False, Sufficiency_of_mobilization=False,
                                                  Previous_service_record=False,
                                                  in_coures=True, Gordan=bat, Religion='اهل تسنن').all().count()
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
            'statistics': statistics,
            'en': settings,
            'total_salme': total_salme,
            'total_gorh_be': total_gorh_be,
            'total_moaf_az_razm': total_moaf_az_razm,
            'total_moaf_az_razm_groh_be': total_moaf_az_razm_groh_be,
            'total_shie': total_shie,
            'total_ahle_tasnon': total_ahle_tasnon,
            'total_soldire': total_soldire,
            'total_amrie_dar': total_amrie_dar,
        }

        return render(request, 'ensani_statistics/vaziate_avalie.html', context)
    else:
        # ابتدا تمام گردان‌ها را بازیابی می‌کنیم
        battalions = battalion.objects.all()
        for bat in battalions:
            # دریافت همه گروهان‌های مربوط به این گردان
            groups = battalion_group.objects.filter(gordan=bat)
            total_soldiers = Soldier.objects.filter(t_Gordan=bat, willing_to_learn=True, IsCheckout=False,
                                                    the_medical_commission=False).all().count()
            battalion_name = bat.name
            lst = []
            salem = Soldier.objects.filter(t_Gordan=bat, physical_condition='سالم',
                                           willing_to_learn=True, IsCheckout=False,
                                           the_medical_commission=False, tatbigh=True).all().count()
            moaf_az_razm = Soldier.objects.filter(t_Gordan=bat, physical_condition='معاف از رزم',
                                                  willing_to_learn=True, IsCheckout=False,
                                                  the_medical_commission=False, tatbigh=True).all().count()
            goreh_b = Soldier.objects.filter(t_Gordan=bat, physical_condition='گروه ب',
                                             willing_to_learn=True, IsCheckout=False,
                                             the_medical_commission=False, tatbigh=True).all().count()
            goreh_b_moaf_az_razm = Soldier.objects.filter(t_Gordan=bat,
                                                          physical_condition='معاف+گروه ب',
                                                          willing_to_learn=True, IsCheckout=False,
                                                          the_medical_commission=False, tatbigh=True).all().count()
            amire_dar = Soldier.objects.filter(t_Gordan=bat, Amriye=True, willing_to_learn=True, IsCheckout=False,
                                               the_medical_commission=False, tatbigh=True).all().count()
            shie = Soldier.objects.filter(t_Gordan=bat, Religion='شیعه', willing_to_learn=True, IsCheckout=False,
                                          the_medical_commission=False, tatbigh=True).all().count()
            ahle_tasanon = Soldier.objects.filter(t_Gordan=bat, Religion='اهل تسنن',
                                                  willing_to_learn=True, IsCheckout=False,
                                                  the_medical_commission=False, tatbigh=True).all().count()
            for group in groups:
                # محاسبه تعداد سربازان برای هر گروهان
                soldiers = Soldier.objects.filter(t_battalion_group=group, willing_to_learn=True,
                                                  the_medical_commission=False, IsCheckout=False)

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
            'statistics': statistics,
            'en': settings,
            'total_salme': total_salme,
            'total_gorh_be': total_gorh_be,
            'total_moaf_az_razm': total_moaf_az_razm,
            'total_moaf_az_razm_groh_be': total_moaf_az_razm_groh_be,
            'total_shie': total_shie,
            'total_ahle_tasnon': total_ahle_tasnon,
            'total_soldire': total_soldire,
            'total_amrie_dar': total_amrie_dar,
        }

        return render(request, 'ensani_statistics/vaziate_avalie.html', context)


@login_required
def amar_gordan_gorhan(request):
    settings = EnsaniSettings.objects.filter().first()
    if settings is None:
        return HttpResponse("تنظیمات دوره انجام نشده!")

    if settings.tatbigh == False:
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
                doctra += soldiers.filter(Grade="دکتری").all().count()
                degrees = soldiers.aggregate(
                    zirediplom=Count(Case(When(Grade='زیر دیپلم', then=1))),
                    diplom=Count(Case(When(Grade='دیپلم', then=1))),
                    ofghdiplom=Count(Case(When(Grade='فوق دیپلم', then=1))),
                    lisans=Count(Case(When(Grade='لیسانس', then=1))),
                    ofghlisans=Count(Case(When(Grade='فوق لیسانس', then=1))),
                    doctra=Count(Case(When(Grade='دکتری', then=1))),
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
            'stats': stats,
            "en": settings
        }
        return render(request, 'ensani_statistics/amar_gordan_gorhan.html', context)
    else:
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
                soldiers = Soldier.objects.filter(t_battalion_group=group, IsCheckout=False,
                                                  the_medical_commission=False, willing_to_learn=True)
                zirediplom += soldiers.filter(Grade="زیر دیپلم").all().count()
                diplom += soldiers.filter(Grade="دیپلم").all().count()
                ofghdiplom += soldiers.filter(Grade="فوق دیپلم").all().count()
                lisans += soldiers.filter(Grade="لیسانس").all().count()
                ofghlisans += soldiers.filter(Grade="فوق لیسانس").all().count()
                doctra += soldiers.filter(Grade="دکتری").all().count()
                degrees = soldiers.aggregate(
                    zirediplom=Count(Case(When(Grade='زیر دیپلم', then=1))),
                    diplom=Count(Case(When(Grade='دیپلم', then=1))),
                    ofghdiplom=Count(Case(When(Grade='فوق دیپلم', then=1))),
                    lisans=Count(Case(When(Grade='لیسانس', then=1))),
                    ofghlisans=Count(Case(When(Grade='فوق لیسانس', then=1))),
                    doctra=Count(Case(When(Grade='دکتری', then=1))),
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
            'stats': stats,
            "en": settings
        }
        return render(request, 'ensani_statistics/amar_gordan_gorhan.html', context)


@login_required
def amar_be_tafkik_madrk_tahsili(request):
    return render(request, 'ensani_statistics/amar_be_tafkik_madrak_tahsili.html')


@login_required
def gozaresh_shoro_dore(request):
    amare_paziresh_shode = Soldier.objects.filter(has_been_accepted=True).all().count()
    salem = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                   physical_condition='سالم',
                                   Sufficiency_of_mobilization=False, Amriye=False,
                                   Previous_service_record=False).all().count()
    moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='معاف از رزم',
                                          Sufficiency_of_mobilization=False, Amriye=False,
                                          Previous_service_record=False).all().count()
    gore_be = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='گروه ب',
                                     Sufficiency_of_mobilization=False, Amriye=False,
                                     Previous_service_record=False).all().count()
    gore_be_moafezrazm = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                physical_condition='معاف+گروه ب',
                                                Sufficiency_of_mobilization=False, Amriye=False,
                                                Previous_service_record=False).all().count()
    Sufficiency_of_mobilization = Soldier.objects.filter(has_been_accepted=True,
                                                         Sufficiency_of_mobilization=True, Amriye=False).all().count()
    Previous_service_record = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True,
                                                     Sufficiency_of_mobilization=False, Amriye=False).all().count()
    comision_shoro_dore = NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی",
                                                            soldire__the_medical_commission=True,
                                                            soldire__Amriye=False).all().count()
    total_1 = int(salem) + int(moaf_az_razm) + int(gore_be) + int(gore_be_moafezrazm) + int(
        Sufficiency_of_mobilization) + int(comision_shoro_dore) + int(
        Previous_service_record)
    total_2 = int(Sufficiency_of_mobilization) + int(comision_shoro_dore) + int(Previous_service_record)

    a_salem = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='سالم',
                                     Sufficiency_of_mobilization=False, Amriye=True,
                                     Previous_service_record=False).all().count()
    a_moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='معاف از رزم',
                                            Sufficiency_of_mobilization=False, Amriye=True,
                                            Previous_service_record=False).all().count()
    a_gorh_be = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='گروه ب',
                                       Sufficiency_of_mobilization=False, Amriye=True,
                                       Previous_service_record=False).all().count()
    a_goreh_be_moh_az_razm = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                    physical_condition='معاف+گروه ب',
                                                    Sufficiency_of_mobilization=False, Amriye=True,
                                                    Previous_service_record=False).all().count()
    a_Sufficiency_of_mobilization = Soldier.objects.filter(has_been_accepted=True,
                                                           Sufficiency_of_mobilization=True, Amriye=True).all().count()
    a_Previous_service_record = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True,
                                                       Sufficiency_of_mobilization=False, Amriye=True).all().count()
    a_comision_shoro_dore = NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی",
                                                              soldire__the_medical_commission=True,
                                                              soldire__Amriye=True).all().count()
    a_total_1 = int(a_salem) + int(a_moaf_az_razm) + int(a_gorh_be) + int(
        a_goreh_be_moh_az_razm) + int(a_Sufficiency_of_mobilization) + int(
        a_comision_shoro_dore) + int(
        a_Previous_service_record)
    a_total_2 = int(a_Sufficiency_of_mobilization) + int(a_comision_shoro_dore) + int(a_Previous_service_record)
    total_kaheshi = a_total_2 + total_2
    shor_dore = (a_total_1 + total_1) - (total_2 + a_total_2)
    a_zire_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='زیر دیپلم').count()
    a_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='دیپلم').count()
    a_fogh_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='فوق دیپلم').count()
    a_lisans = Soldier.objects.filter(has_been_accepted=True, Grade_precise='لیسانس').count()
    a_fogh_lisans = Soldier.objects.filter(has_been_accepted=True, Grade_precise='فوق لیسانس').count()
    a_doctora = Soldier.objects.filter(has_been_accepted=True, Grade_precise='دکتری').count()
    a_bisavad = Soldier.objects.filter(has_been_accepted=True, Grade_precise='بی‌سواد').count()
    a_nehzad = Soldier.objects.filter(has_been_accepted=True, Grade_precise='نهضت سواد آموزی').count()
    a_rahinami = Soldier.objects.filter(has_been_accepted=True, Grade_precise='راهنمایی').count()
    a_sikel = Soldier.objects.filter(has_been_accepted=True, Grade_precise='سیکل').count()
    a_dabirestan = Soldier.objects.filter(has_been_accepted=True, Grade_precise='دبیرستان').count()
    a_ebtedai = Soldier.objects.filter(has_been_accepted=True, Grade_precise='ابتدایی').count()
    a_total = int(a_zire_diplom) + int(a_diplom) + int(a_fogh_diplom) + int(a_lisans) + int(a_fogh_lisans) + int(
        a_doctora) + int(a_bisavad) + int(a_nehzad) + int(a_rahinami) + int(a_sikel) + int(a_dabirestan) + int(
        a_ebtedai)
    in_course_zire_diplom = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                   Grade_precise='زیر دیپلم').count()
    in_course_diplom = Soldier.objects.filter(has_been_accepted=True, in_coures=True, Grade_precise='دیپلم').count()
    in_course_fogh_diplom = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                   Grade_precise='فوق دیپلم').count()
    in_course_lisans = Soldier.objects.filter(has_been_accepted=True, in_coures=True, Grade_precise='لیسانس').count()
    in_course_fogh_lisans = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                   Grade_precise='فوق لیسانس').count()
    in_course_doctora = Soldier.objects.filter(has_been_accepted=True, in_coures=True, Grade_precise='دکتری').count()
    in_course_bisavad = Soldier.objects.filter(has_been_accepted=True, in_coures=True, Grade_precise='بی‌سواد').count()
    in_course_nehzad = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                              Grade_precise='نهضت سواد آموزی').count()
    in_course_rahinami = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                Grade_precise='راهنمایی').count()
    in_course_sikel = Soldier.objects.filter(has_been_accepted=True, in_coures=True, Grade_precise='سیکل').count()
    in_course_dabirestan = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                  Grade_precise='دبیرستان').count()
    in_course_ebtedai = Soldier.objects.filter(has_been_accepted=True, in_coures=True, Grade_precise='ابتدایی').count()

    in_courese_total = int(in_course_zire_diplom) + int(in_course_diplom) + int(in_course_fogh_diplom) + int(
        in_course_lisans) + int(in_course_fogh_lisans) + int(in_course_doctora) + int(
        in_course_bisavad) + int(in_course_nehzad) + int(in_course_rahinami) + int(in_course_sikel) + int(
        in_course_dabirestan) + int(in_course_ebtedai)
    en = EnsaniSettings.objects.filter().first()
    cx = {

        'salem': salem,
        'moaf_az_razm': moaf_az_razm,
        'amare_paziresh_shode': amare_paziresh_shode,
        'Sufficiency_of_mobilization': Sufficiency_of_mobilization,
        'Previous_service_record': Previous_service_record,
        'comision_shoro_dore': comision_shoro_dore,
        'total_1': total_1,
        'total_2': total_2,
        'asalem': a_salem,
        'amoaf_az_razm': a_moaf_az_razm,
        'aSufficiency_of_mobilization': a_Sufficiency_of_mobilization,
        'aPrevious_service_record': a_Previous_service_record,
        'acomision_shoro_dore': a_comision_shoro_dore,
        'atotal_1': a_total_1,
        'atotal_2': a_total_2,
        'total_kaheshi': total_kaheshi,
        'shor_dore': shor_dore,
        'a_zire_diplom': a_zire_diplom,
        'a_diplom': a_diplom,
        'a_fogh_diplom': a_fogh_diplom,
        'a_lisans': a_lisans,
        'a_fogh_lisans': a_fogh_lisans,
        'a_doctora': a_doctora,
        'a_bisavad': a_bisavad + a_zire_diplom,
        'a_nehzad': a_nehzad,
        'a_rahinami': a_rahinami,
        'a_sikel': a_sikel,
        'a_dabirestan': a_dabirestan,
        'a_ebtedai': a_ebtedai,
        'a_total': a_total,
        'in_course_zire_diplom': in_course_zire_diplom,
        'in_course_diplom': in_course_diplom,
        'in_course_fogh_diplom': in_course_fogh_diplom,
        'in_course_lisans': in_course_lisans,
        'in_course_fogh_lisans': in_course_fogh_lisans,
        'in_course_doctora': in_course_doctora,
        'in_course_bisavad': in_course_bisavad + in_course_zire_diplom,
        'in_course_nehzad': in_course_nehzad,
        'in_course_rahinami': in_course_rahinami,
        'in_course_sikel': in_course_sikel,
        'in_course_dabirestan': in_course_dabirestan,
        'in_course_ebtedai': in_course_ebtedai,
        'in_courese_total': in_courese_total,
        'en': en,

    }
    return render(request, 'ensani_statistics/gozaresh_shoro_dore.html', cx)


@login_required
def amar_shoro_doreh(request):
    amare_paziresh_shode = Soldier.objects.filter(has_been_accepted=True).all().count()
    salem = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                   physical_condition='سالم',
                                   Sufficiency_of_mobilization=False, Amriye=False,
                                   Previous_service_record=False).all().count()
    moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='معاف از رزم',
                                          Sufficiency_of_mobilization=False, Amriye=False,
                                          Previous_service_record=False).all().count()
    Sufficiency_of_mobilization = Soldier.objects.filter(has_been_accepted=True,
                                                         Sufficiency_of_mobilization=True, Amriye=False).all().count()
    Previous_service_record = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True,
                                                     Sufficiency_of_mobilization=False, Amriye=False).all().count()
    comision_shoro_dore = NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی",
                                                            soldire__the_medical_commission=True,
                                                            soldire__Amriye=False).all().count()
    total_1 = int(salem) + int(moaf_az_razm) + int(Sufficiency_of_mobilization) + int(comision_shoro_dore) + int(
        Previous_service_record)
    total_2 = int(Sufficiency_of_mobilization) + int(comision_shoro_dore) + int(Previous_service_record)

    a_salem = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='سالم',
                                     Sufficiency_of_mobilization=False, Amriye=True,
                                     Previous_service_record=False).all().count()
    a_moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='معاف از رزم',
                                            Sufficiency_of_mobilization=False, Amriye=True,
                                            Previous_service_record=False).all().count()

    a_Sufficiency_of_mobilization = Soldier.objects.filter(has_been_accepted=True,
                                                           Sufficiency_of_mobilization=True, Amriye=True).all().count()
    a_Previous_service_record = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True,
                                                       Sufficiency_of_mobilization=False, Amriye=True).all().count()
    a_comision_shoro_dore = NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی",
                                                              soldire__the_medical_commission=True,
                                                              soldire__Amriye=True).all().count()
    a_total_1 = int(a_salem) + int(a_moaf_az_razm) + int(a_Sufficiency_of_mobilization) + int(
        a_comision_shoro_dore) + int(
        a_Previous_service_record)
    a_total_2 = int(a_Sufficiency_of_mobilization) + int(a_comision_shoro_dore) + int(a_Previous_service_record)
    total_kaheshi = a_total_2 + total_2
    shor_dore = (a_total_1 + total_1) - (total_2 + a_total_2)
    cx = {
        'salem': salem,
        'moaf_az_razm': moaf_az_razm,
        'amare_paziresh_shode': amare_paziresh_shode,
        'Sufficiency_of_mobilization': Sufficiency_of_mobilization,
        'Previous_service_record': Previous_service_record,
        'comision_shoro_dore': comision_shoro_dore,
        'total_1': total_1,
        'total_2': total_2,
        'asalem': a_salem,
        'amoaf_az_razm': a_moaf_az_razm,
        'aSufficiency_of_mobilization': a_Sufficiency_of_mobilization,
        'aPrevious_service_record': a_Previous_service_record,
        'acomision_shoro_dore': a_comision_shoro_dore,
        'atotal_1': a_total_1,
        'atotal_2': a_total_2,
        'total_kaheshi': total_kaheshi,
        'shor_dore': shor_dore
    }
    return render(request, 'ensani_statistics/amar_shoro_doreh.html', cx)


@login_required
def amar_payan_dore(request):
    amare_paziresh_shode = Soldier.objects.filter(has_been_accepted=True).all().count()
    salem = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                   physical_condition='سالم',
                                   Sufficiency_of_mobilization=False, Amriye=False).all().count()
    moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                          physical_condition='معاف از رزم',
                                          Sufficiency_of_mobilization=False, Amriye=False,
                                          ).all().count()
    groh_be = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                     physical_condition='گروه ب',
                                     Sufficiency_of_mobilization=False, Amriye=False,
                                     ).all().count()
    moaf_az_razm_groh_be = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                                  physical_condition='معاف+گروه ب',
                                                  Sufficiency_of_mobilization=False, Amriye=False,
                                                  ).all().count()
    Sufficiency_of_mobilization = Soldier.objects.filter(has_been_accepted=True,
                                                         Sufficiency_of_mobilization=True, Amriye=False).all().count()
    Previous_service_record = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True,
                                                     Sufficiency_of_mobilization=False, Amriye=False).all().count()
    comision = Soldier.objects.filter(the_medical_commission=True, IsCheckout=True).all().count()
    isChkeckout = Soldier.objects.filter(IsCheckout=True, the_medical_commission=False, Amriye=False).all().count()

    total_1 = int(salem) + int(moaf_az_razm) + int(moaf_az_razm_groh_be) + int(groh_be) + int(comision) + int(
        Previous_service_record)
    total_2 = int(isChkeckout) + int(comision)
    a_salem = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                     physical_condition='سالم',
                                     Sufficiency_of_mobilization=False, Amriye=True).all().count()
    a_moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                            physical_condition='معاف از رزم',
                                            Sufficiency_of_mobilization=False, Amriye=True).all().count()
    a_groh_be = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                       physical_condition='گروه ب',
                                       Sufficiency_of_mobilization=False, Amriye=True).all().count()
    a_moaf_az_razm_groh_be = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
                                                    physical_condition='معاف+گروه ب',
                                                    Sufficiency_of_mobilization=False, Amriye=True).all().count()
    a_Sufficiency_of_mobilization = Soldier.objects.filter(has_been_accepted=True,
                                                           Sufficiency_of_mobilization=True, Amriye=True).all().count()
    a_Previous_service_record = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True,
                                                       Sufficiency_of_mobilization=False, Amriye=True).all().count()
    a_comision = Soldier.objects.filter(the_medical_commission=True, IsCheckout=True, Amriye=True).all().count()
    a_isChkeckout = Soldier.objects.filter(IsCheckout=True, the_medical_commission=False, Amriye=True).all().count()
    a_total_1 = int(a_salem) + int(a_moaf_az_razm) + int(a_groh_be) + int(
        a_comision) + int(
        a_moaf_az_razm_groh_be)
    a_total_2 = int(a_Sufficiency_of_mobilization) + int(a_comision) + int(a_isChkeckout)
    total_kaheshi = a_total_2 + total_2
    shor_dore = Soldier.objects.filter(has_been_accepted=True, in_coures=True).all().count()
    payandore = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True).all().count()
    cx = {
        'salem': salem,
        'moaf_az_razm': moaf_az_razm,
        'amare_paziresh_shode': amare_paziresh_shode,
        'Sufficiency_of_mobilization': Sufficiency_of_mobilization,
        'Previous_service_record': Previous_service_record,
        'comision': comision,
        'groh_be': groh_be,
        'moaf_az_razm_groh_be': moaf_az_razm_groh_be,
        'total_1': total_1,
        'total_2': total_2,
        'asalem': a_salem,
        'amoaf_az_razm': a_moaf_az_razm,
        'aSufficiency_of_mobilization': a_Sufficiency_of_mobilization,
        'aPrevious_service_record': a_Previous_service_record,
        'a_comision': a_comision,
        'atotal_1': a_total_1,
        'atotal_2': a_total_2,
        'total_kaheshi': total_kaheshi,
        'shor_dore': shor_dore,
        'isChkeckout': isChkeckout,
        'a_isChkeckout': a_isChkeckout,
        'a_groh_be': a_groh_be,
        'a_moaf_az_razm_groh_be': a_moaf_az_razm_groh_be,
        'payandore': payandore,

    }

    return render(request, 'ensani_statistics/amar_payan_dore.html', cx)


@login_required
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


@login_required
def amar_avalie_samane_baghimonde(request):
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
        total = Soldier.objects.filter(province_name=province, has_been_accepted=False).count()
        salem = Soldier.objects.filter(province_name=province, physical_condition='سالم',
                                       has_been_accepted=False).count()
        moaf_az_razm = Soldier.objects.filter(province_name=province, physical_condition='معاف از رزم',
                                              has_been_accepted=False).count()
        goreh_b = Soldier.objects.filter(province_name=province, physical_condition='گروه ب',
                                         has_been_accepted=False).count()
        goreh_b_moaf_az_razm = Soldier.objects.filter(province_name=province, physical_condition='معاف+گروه ب',
                                                      has_been_accepted=False).count()
        amire_dar = Soldier.objects.filter(province_name=province, Amriye=True, has_been_accepted=False).count()
        shie = Soldier.objects.filter(province_name=province, Religion='شیعه', has_been_accepted=False).count()
        ahle_tasanon = Soldier.objects.filter(province_name=province, Religion='اهل تسنن',
                                              has_been_accepted=False).count()
        zire_diplom = Soldier.objects.filter(province_name=province, Grade='زیر دیپلم', has_been_accepted=False).count()
        diplom = Soldier.objects.filter(province_name=province, Grade='دیپلم', has_been_accepted=False).count()
        fogh_diplom = Soldier.objects.filter(province_name=province, Grade='فوق دیپلم', has_been_accepted=False).count()
        lisans = Soldier.objects.filter(province_name=province, Grade='لیسانس', has_been_accepted=False).count()
        fogh_lisans = Soldier.objects.filter(province_name=province, Grade='فوق لیسانس',
                                             has_been_accepted=False).count()
        doctora = Soldier.objects.filter(province_name=province, Grade='دکتری', has_been_accepted=False).count()
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
    soldire_total = Soldier.objects.filter(date_improt_type='سامانه', has_been_accepted=False).all().count()
    soldire_total_salem = Soldier.objects.filter(date_improt_type='سامانه', physical_condition='سالم',
                                                 has_been_accepted=False).all().count()
    soldire_total_moafazrazm = Soldier.objects.filter(date_improt_type='سامانه',
                                                      physical_condition='معاف از رزم',
                                                      has_been_accepted=False).all().count()
    soldire_total_shie = Soldier.objects.filter(date_improt_type='سامانه', Religion='شیعه',
                                                has_been_accepted=False).all().count()
    soldire_total_tasanon = Soldier.objects.filter(date_improt_type='سامانه', Religion='اهل تسنن',
                                                   has_been_accepted=False).all().count()
    soldire_total_amire = Soldier.objects.filter(date_improt_type='سامانه', Amriye=True,
                                                 has_been_accepted=False).all().count()
    zire_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='زیر دیپلم', has_been_accepted=False).count()
    diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='دیپلم', has_been_accepted=False).count()
    fogh_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق دیپلم', has_been_accepted=False).count()
    lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='لیسانس', has_been_accepted=False).count()
    fogh_lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق لیسانس', has_been_accepted=False).count()
    doctora = Soldier.objects.filter(date_improt_type='سامانه', Grade='دکتری', has_been_accepted=False).count()
    namoshakhas = Soldier.objects.filter(date_improt_type='سامانه', Grade='نامشخص', has_been_accepted=False).count()
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
    return render(request, 'ensani_statistics/amar_samane_baghimonde.html', cx)


@login_required
def amar_avalie_samane_paziresh_shode(request):
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
        total = Soldier.objects.filter(province_name=province, has_been_accepted=True).count()
        salem = Soldier.objects.filter(province_name=province, physical_condition='سالم',
                                       has_been_accepted=True).count()
        moaf_az_razm = Soldier.objects.filter(province_name=province, physical_condition='معاف از رزم',
                                              has_been_accepted=True).count()
        goreh_b = Soldier.objects.filter(province_name=province, physical_condition='گروه ب',
                                         has_been_accepted=False).count()
        goreh_b_moaf_az_razm = Soldier.objects.filter(province_name=province, physical_condition='معاف+گروه ب',
                                                      has_been_accepted=True).count()
        amire_dar = Soldier.objects.filter(province_name=province, Amriye=True, has_been_accepted=True).count()
        shie = Soldier.objects.filter(province_name=province, Religion='شیعه', has_been_accepted=True).count()
        ahle_tasanon = Soldier.objects.filter(province_name=province, Religion='اهل تسنن',
                                              has_been_accepted=True).count()
        zire_diplom = Soldier.objects.filter(province_name=province, Grade='زیر دیپلم', has_been_accepted=True).count()
        diplom = Soldier.objects.filter(province_name=province, Grade='دیپلم', has_been_accepted=True).count()
        fogh_diplom = Soldier.objects.filter(province_name=province, Grade='فوق دیپلم', has_been_accepted=True).count()
        lisans = Soldier.objects.filter(province_name=province, Grade='لیسانس', has_been_accepted=True).count()
        fogh_lisans = Soldier.objects.filter(province_name=province, Grade='فوق لیسانس', has_been_accepted=True).count()
        doctora = Soldier.objects.filter(province_name=province, Grade='دکتری', has_been_accepted=True).count()
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
    soldire_total = Soldier.objects.filter(date_improt_type='سامانه', has_been_accepted=True).all().count()
    soldire_total_salem = Soldier.objects.filter(date_improt_type='سامانه', physical_condition='سالم',
                                                 has_been_accepted=True).all().count()
    soldire_total_moafazrazm = Soldier.objects.filter(date_improt_type='سامانه',
                                                      physical_condition='معاف از رزم',
                                                      has_been_accepted=True).all().count()
    soldire_total_shie = Soldier.objects.filter(date_improt_type='سامانه', Religion='شیعه',
                                                has_been_accepted=True).all().count()
    soldire_total_tasanon = Soldier.objects.filter(date_improt_type='سامانه', Religion='اهل تسنن',
                                                   has_been_accepted=True).all().count()
    soldire_total_amire = Soldier.objects.filter(date_improt_type='سامانه', Amriye=True,
                                                 has_been_accepted=True).all().count()
    zire_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='زیر دیپلم', has_been_accepted=True).count()
    diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='دیپلم', has_been_accepted=True).count()
    fogh_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق دیپلم', has_been_accepted=True).count()
    lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='لیسانس', has_been_accepted=True).count()
    fogh_lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق لیسانس', has_been_accepted=True).count()
    doctora = Soldier.objects.filter(date_improt_type='سامانه', Grade='دکتری', has_been_accepted=True).count()
    namoshakhas = Soldier.objects.filter(date_improt_type='سامانه', Grade='نامشخص', has_been_accepted=True).count()
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
    return render(request, 'ensani_statistics/amare_samane_paziresh_shode.html', cx)


@login_required
def yegan_be_kar_girande(request):
    return render(request, 'ensani_statistics/gozaresh_yeghan_be_kar_girande.html')


@login_required
def yegan_be_kar_girande_tabel(request):
    salem_in_course_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                              in_coures=True, physical_condition='سالم',
                                                              unit_type='سپاه و رده های اقماری').all().count()
    moaf_az_razm_in_course_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                                     in_coures=True, physical_condition='معاف از رزم',
                                                                     unit_type='سپاه و رده های اقماری').all().count()
    groh_be_in_course_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                                in_coures=True, physical_condition='گروه ب',
                                                                unit_type='سپاه و رده های اقماری').all().count()
    moaf_az_razm_gorh_be_in_course_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                             willing_to_learn=True,
                                                                             in_coures=True,
                                                                             physical_condition='معاف+گروه ب',
                                                                             unit_type='سپاه و رده های اقماری').all().count()
    total1_in_course_pa_radeh_aghmari = int(moaf_az_razm_in_course_pa_radeh_aghmari) + int(
        groh_be_in_course_pa_radeh_aghmari) + int(moaf_az_razm_gorh_be_in_course_pa_radeh_aghmari)
    total2_in_course_pa_radeh_aghmari = int(salem_in_course_pa_radeh_aghmari) + int(
        moaf_az_razm_in_course_pa_radeh_aghmari) + int(
        groh_be_in_course_pa_radeh_aghmari) + int(moaf_az_razm_gorh_be_in_course_pa_radeh_aghmari)

    salem_Previous_service_record_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                            physical_condition='سالم',
                                                                            unit_type='سپاه و رده های اقماری',
                                                                            Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                                   physical_condition='معاف از رزم',
                                                                                   unit_type='سپاه و رده های اقماری',
                                                                                   Previous_service_record=True).all().count()
    groh_be_Previous_service_record_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                              physical_condition='گروه ب',
                                                                              unit_type='سپاه و رده های اقماری',
                                                                              Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                                           physical_condition='معاف+گروه ب',
                                                                                           unit_type='سپاه و رده های اقماری',
                                                                                           Previous_service_record=True).all().count()
    total1_Previous_service_record_pa_radeh_aghmari = int(moaf_az_razm_Previous_service_record_pa_radeh_aghmari) + int(
        groh_be_Previous_service_record_pa_radeh_aghmari) + int(
        moaf_az_razm_gorh_be_Previous_service_record_pa_radeh_aghmari)
    total2_Previous_service_record_pa_radeh_aghmari = int(salem_Previous_service_record_pa_radeh_aghmari) + int(
        moaf_az_razm_Previous_service_record_pa_radeh_aghmari) + int(
        groh_be_Previous_service_record_pa_radeh_aghmari) + int(
        moaf_az_razm_gorh_be_Previous_service_record_pa_radeh_aghmari)

    salem_Sufficiency_of_mobilization_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                                physical_condition='سالم',
                                                                                unit_type='سپاه و رده های اقماری',
                                                                                Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                                       physical_condition='معاف از رزم',
                                                                                       unit_type='سپاه و رده های اقماری',
                                                                                       Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                                  physical_condition='گروه ب',
                                                                                  unit_type='سپاه و رده های اقماری',
                                                                                  Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                                                               physical_condition='معاف+گروه ب',
                                                                                               unit_type='سپاه و رده های اقماری',
                                                                                               Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_pa_radeh_aghmari = int(
        moaf_az_razm_Sufficiency_of_mobilization_pa_radeh_aghmari) + int(
        groh_be_Sufficiency_of_mobilization_pa_radeh_aghmari) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_pa_radeh_aghmari)
    total2_Sufficiency_of_mobilization_pa_radeh_aghmari = int(salem_Sufficiency_of_mobilization_pa_radeh_aghmari) + int(
        moaf_az_razm_Sufficiency_of_mobilization_pa_radeh_aghmari) + int(
        groh_be_Sufficiency_of_mobilization_pa_radeh_aghmari) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_pa_radeh_aghmari)
    total_pa_radeh_aghmari = Soldier.objects.filter(has_been_accepted=True,
                                                    unit_type='سپاه و رده های اقماری').all().count()

    # نزسا
    salem_in_course_nezsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                   in_coures=True, physical_condition='سالم',
                                                   unit_type='نزسا').all().count()
    moaf_az_razm_in_course_nezsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                          in_coures=True, physical_condition='معاف از رزم',
                                                          unit_type='نزسا').all().count()
    groh_be_in_course_nezsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                     in_coures=True, physical_condition='گروه ب',
                                                     unit_type='نزسا').all().count()
    moaf_az_razm_gorh_be_in_course_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                  willing_to_learn=True,
                                                                  in_coures=True,
                                                                  physical_condition='معاف+گروه ب',
                                                                  unit_type='نزسا').all().count()
    total1_in_course_nezsa = int(moaf_az_razm_in_course_nezsa) + int(
        groh_be_in_course_nezsa) + int(moaf_az_razm_gorh_be_in_course_nezsa)
    total2_in_course_nezsa = int(salem_in_course_nezsa) + int(
        moaf_az_razm_in_course_nezsa) + int(
        groh_be_in_course_nezsa) + int(moaf_az_razm_gorh_be_in_course_nezsa)

    salem_Previous_service_record_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                 physical_condition='سالم',
                                                                 unit_type='نزسا',
                                                                 Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                        physical_condition='معاف از رزم',
                                                                        unit_type='نزسا',
                                                                        Previous_service_record=True).all().count()
    groh_be_Previous_service_record_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                   physical_condition='گروه ب',
                                                                   unit_type='نزسا',
                                                                   Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                                physical_condition='معاف+گروه ب',
                                                                                unit_type='نزسا',
                                                                                Previous_service_record=True).all().count()
    total1_Previous_service_record_nezsa = int(moaf_az_razm_Previous_service_record_nezsa) + int(
        groh_be_Previous_service_record_nezsa) + int(
        moaf_az_razm_gorh_be_Previous_service_record_nezsa)
    total2_Previous_service_record_nezsa = int(salem_Previous_service_record_nezsa) + int(
        moaf_az_razm_Previous_service_record_nezsa) + int(
        groh_be_Previous_service_record_nezsa) + int(
        moaf_az_razm_gorh_be_Previous_service_record_nezsa)

    salem_Sufficiency_of_mobilization_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                     physical_condition='سالم',
                                                                     unit_type='نزسا',
                                                                     Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                            physical_condition='معاف از رزم',
                                                                            unit_type='نزسا',
                                                                            Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                       physical_condition='گروه ب',
                                                                       unit_type='نزسا',
                                                                       Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                                                                    physical_condition='معاف+گروه ب',
                                                                                    unit_type='نزسا',
                                                                                    Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_nezsa = int(
        moaf_az_razm_Sufficiency_of_mobilization_nezsa) + int(
        groh_be_Sufficiency_of_mobilization_nezsa) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_nezsa)
    total2_Sufficiency_of_mobilization_nezsa = int(salem_Sufficiency_of_mobilization_nezsa) + int(
        moaf_az_razm_Sufficiency_of_mobilization_nezsa) + int(
        groh_be_Sufficiency_of_mobilization_nezsa) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_nezsa)
    total_nezsa = Soldier.objects.filter(has_been_accepted=True,
                                         unit_type='نزسا').all().count()
    # نقسا
    salem_in_course_neghsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                    in_coures=True, physical_condition='سالم',
                                                    unit_type='نقسا').all().count()
    moaf_az_razm_in_course_neghsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                           in_coures=True, physical_condition='معاف از رزم',
                                                           unit_type='نقسا').all().count()
    groh_be_in_course_neghsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                      in_coures=True, physical_condition='گروه ب',
                                                      unit_type='نقسا').all().count()
    moaf_az_razm_gorh_be_in_course_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                   willing_to_learn=True,
                                                                   in_coures=True,
                                                                   physical_condition='معاف+گروه ب',
                                                                   unit_type='نقسا').all().count()
    total1_in_course_neghsa = int(moaf_az_razm_in_course_neghsa) + int(
        groh_be_in_course_neghsa) + int(moaf_az_razm_gorh_be_in_course_neghsa)
    total2_in_course_neghsa = int(salem_in_course_neghsa) + int(
        moaf_az_razm_in_course_neghsa) + int(
        groh_be_in_course_neghsa) + int(moaf_az_razm_gorh_be_in_course_neghsa)

    salem_Previous_service_record_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                  physical_condition='سالم',
                                                                  unit_type='نقسا',
                                                                  Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                         physical_condition='معاف از رزم',
                                                                         unit_type='نقسا',
                                                                         Previous_service_record=True).all().count()
    groh_be_Previous_service_record_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                    physical_condition='گروه ب',
                                                                    unit_type='نقسا',
                                                                    Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                                 physical_condition='معاف+گروه ب',
                                                                                 unit_type='نقسا',
                                                                                 Previous_service_record=True).all().count()
    total1_Previous_service_record_neghsa = int(moaf_az_razm_Previous_service_record_neghsa) + int(
        groh_be_Previous_service_record_neghsa) + int(
        moaf_az_razm_gorh_be_Previous_service_record_neghsa)
    total2_Previous_service_record_neghsa = int(salem_Previous_service_record_neghsa) + int(
        moaf_az_razm_Previous_service_record_neghsa) + int(
        groh_be_Previous_service_record_neghsa) + int(
        moaf_az_razm_gorh_be_Previous_service_record_neghsa)

    salem_Sufficiency_of_mobilization_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                      physical_condition='سالم',
                                                                      unit_type='نقسا',
                                                                      Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                             physical_condition='معاف از رزم',
                                                                             unit_type='نقسا',
                                                                             Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                        physical_condition='گروه ب',
                                                                        unit_type='نقسا',
                                                                        Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                                                                     physical_condition='معاف+گروه ب',
                                                                                     unit_type='نقسا',
                                                                                     Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_neghsa = int(
        moaf_az_razm_Sufficiency_of_mobilization_neghsa) + int(
        groh_be_Sufficiency_of_mobilization_neghsa) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_neghsa)
    total2_Sufficiency_of_mobilization_neghsa = int(salem_Sufficiency_of_mobilization_neghsa) + int(
        moaf_az_razm_Sufficiency_of_mobilization_neghsa) + int(
        groh_be_Sufficiency_of_mobilization_neghsa) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_neghsa)
    total_neghsa = Soldier.objects.filter(has_been_accepted=True,
                                          unit_type='نقسا').all().count()
    # ندسا
    salem_in_course_ndsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                  in_coures=True, physical_condition='سالم',
                                                  unit_type='ندسا').all().count()
    moaf_az_razm_in_course_ndsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                         in_coures=True, physical_condition='معاف از رزم',
                                                         unit_type='ندسا').all().count()
    groh_be_in_course_ndsa = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                    in_coures=True, physical_condition='گروه ب',
                                                    unit_type='ندسا').all().count()
    moaf_az_razm_gorh_be_in_course_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                 willing_to_learn=True,
                                                                 in_coures=True,
                                                                 physical_condition='معاف+گروه ب',
                                                                 unit_type='ندسا').all().count()
    total1_in_course_ndsa = int(moaf_az_razm_in_course_ndsa) + int(
        groh_be_in_course_ndsa) + int(moaf_az_razm_gorh_be_in_course_ndsa)
    total2_in_course_ndsa = int(salem_in_course_ndsa) + int(
        moaf_az_razm_in_course_ndsa) + int(
        groh_be_in_course_ndsa) + int(moaf_az_razm_gorh_be_in_course_ndsa)

    salem_Previous_service_record_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                physical_condition='سالم',
                                                                unit_type='ندسا',
                                                                Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                       physical_condition='معاف از رزم',
                                                                       unit_type='ندسا',
                                                                       Previous_service_record=True).all().count()
    groh_be_Previous_service_record_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                  physical_condition='گروه ب',
                                                                  unit_type='ندسا',
                                                                  Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                               physical_condition='معاف+گروه ب',
                                                                               unit_type='ندسا',
                                                                               Previous_service_record=True).all().count()
    total1_Previous_service_record_ndsa = int(moaf_az_razm_Previous_service_record_ndsa) + int(
        groh_be_Previous_service_record_ndsa) + int(
        moaf_az_razm_gorh_be_Previous_service_record_ndsa)
    total2_Previous_service_record_ndsa = int(salem_Previous_service_record_ndsa) + int(
        moaf_az_razm_Previous_service_record_ndsa) + int(
        groh_be_Previous_service_record_ndsa) + int(
        moaf_az_razm_gorh_be_Previous_service_record_ndsa)

    salem_Sufficiency_of_mobilization_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                    physical_condition='سالم',
                                                                    unit_type='ندسا',
                                                                    Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                           physical_condition='معاف از رزم',
                                                                           unit_type='ندسا',
                                                                           Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                      physical_condition='گروه ب',
                                                                      unit_type='ندسا',
                                                                      Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                                                                   physical_condition='معاف+گروه ب',
                                                                                   unit_type='ندسا',
                                                                                   Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_ndsa = int(
        moaf_az_razm_Sufficiency_of_mobilization_ndsa) + int(
        groh_be_Sufficiency_of_mobilization_ndsa) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_ndsa)
    total2_Sufficiency_of_mobilization_ndsa = int(salem_Sufficiency_of_mobilization_ndsa) + int(
        moaf_az_razm_Sufficiency_of_mobilization_ndsa) + int(
        groh_be_Sufficiency_of_mobilization_ndsa) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_ndsa)
    total_ndsa = Soldier.objects.filter(has_been_accepted=True,
                                        unit_type='ندسا').all().count()
    # هوافضا
    salem_in_course_havafaza = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                      in_coures=True, physical_condition='سالم',
                                                      unit_type='هوافضا').all().count()
    moaf_az_razm_in_course_havafaza = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                             in_coures=True, physical_condition='معاف از رزم',
                                                             unit_type='هوافضا').all().count()
    groh_be_in_course_havafaza = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                        in_coures=True, physical_condition='گروه ب',
                                                        unit_type='هوافضا').all().count()
    moaf_az_razm_gorh_be_in_course_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                     willing_to_learn=True,
                                                                     in_coures=True,
                                                                     physical_condition='معاف+گروه ب',
                                                                     unit_type='هوافضا').all().count()
    total1_in_course_havafaza = int(moaf_az_razm_in_course_havafaza) + int(
        groh_be_in_course_havafaza) + int(moaf_az_razm_gorh_be_in_course_havafaza)
    total2_in_course_havafaza = int(salem_in_course_havafaza) + int(
        moaf_az_razm_in_course_havafaza) + int(
        groh_be_in_course_havafaza) + int(moaf_az_razm_gorh_be_in_course_havafaza)

    salem_Previous_service_record_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                    physical_condition='سالم',
                                                                    unit_type='هوافضا',
                                                                    Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                           physical_condition='معاف از رزم',
                                                                           unit_type='هوافضا',
                                                                           Previous_service_record=True).all().count()
    groh_be_Previous_service_record_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                      physical_condition='گروه ب',
                                                                      unit_type='هوافضا',
                                                                      Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                                   physical_condition='معاف+گروه ب',
                                                                                   unit_type='هوافضا',
                                                                                   Previous_service_record=True).all().count()
    total1_Previous_service_record_havafaza = int(moaf_az_razm_Previous_service_record_havafaza) + int(
        groh_be_Previous_service_record_havafaza) + int(
        moaf_az_razm_gorh_be_Previous_service_record_havafaza)
    total2_Previous_service_record_havafaza = int(salem_Previous_service_record_havafaza) + int(
        moaf_az_razm_Previous_service_record_havafaza) + int(
        groh_be_Previous_service_record_havafaza) + int(
        moaf_az_razm_gorh_be_Previous_service_record_havafaza)

    salem_Sufficiency_of_mobilization_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                        physical_condition='سالم',
                                                                        unit_type='هوافضا',
                                                                        Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                               physical_condition='معاف از رزم',
                                                                               unit_type='هوافضا',
                                                                               Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                          physical_condition='گروه ب',
                                                                          unit_type='هوافضا',
                                                                          Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                                                                       physical_condition='معاف+گروه ب',
                                                                                       unit_type='هوافضا',
                                                                                       Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_havafaza = int(
        moaf_az_razm_Sufficiency_of_mobilization_havafaza) + int(
        groh_be_Sufficiency_of_mobilization_havafaza) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_havafaza)
    total2_Sufficiency_of_mobilization_havafaza = int(salem_Sufficiency_of_mobilization_havafaza) + int(
        moaf_az_razm_Sufficiency_of_mobilization_havafaza) + int(
        groh_be_Sufficiency_of_mobilization_havafaza) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_havafaza)
    total_havafaza = Soldier.objects.filter(has_been_accepted=True,
                                            unit_type='هوافضا').all().count()
    # سازمان بسیج
    salem_in_course_sazman_basij = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                          in_coures=True, physical_condition='سالم',
                                                          unit_type='سازمان بسیج').all().count()
    moaf_az_razm_in_course_sazman_basij = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                                 in_coures=True, physical_condition='معاف از رزم',
                                                                 unit_type='سازمان بسیج').all().count()
    groh_be_in_course_sazman_basij = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                            in_coures=True, physical_condition='گروه ب',
                                                            unit_type='سازمان بسیج').all().count()
    moaf_az_razm_gorh_be_in_course_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                         willing_to_learn=True,
                                                                         in_coures=True,
                                                                         physical_condition='معاف+گروه ب',
                                                                         unit_type='سازمان بسیج').all().count()
    total1_in_course_sazman_basij = int(moaf_az_razm_in_course_sazman_basij) + int(
        groh_be_in_course_sazman_basij) + int(moaf_az_razm_gorh_be_in_course_sazman_basij)
    total2_in_course_sazman_basij = int(salem_in_course_sazman_basij) + int(
        moaf_az_razm_in_course_sazman_basij) + int(
        groh_be_in_course_sazman_basij) + int(moaf_az_razm_gorh_be_in_course_sazman_basij)

    salem_Previous_service_record_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                        physical_condition='سالم',
                                                                        unit_type='سازمان بسیج',
                                                                        Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                               physical_condition='معاف از رزم',
                                                                               unit_type='سازمان بسیج',
                                                                               Previous_service_record=True).all().count()
    groh_be_Previous_service_record_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                          physical_condition='گروه ب',
                                                                          unit_type='سازمان بسیج',
                                                                          Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                                       physical_condition='معاف+گروه ب',
                                                                                       unit_type='سازمان بسیج',
                                                                                       Previous_service_record=True).all().count()
    total1_Previous_service_record_sazman_basij = int(moaf_az_razm_Previous_service_record_sazman_basij) + int(
        groh_be_Previous_service_record_sazman_basij) + int(
        moaf_az_razm_gorh_be_Previous_service_record_sazman_basij)
    total2_Previous_service_record_sazman_basij = int(salem_Previous_service_record_sazman_basij) + int(
        moaf_az_razm_Previous_service_record_sazman_basij) + int(
        groh_be_Previous_service_record_sazman_basij) + int(
        moaf_az_razm_gorh_be_Previous_service_record_sazman_basij)

    salem_Sufficiency_of_mobilization_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                            physical_condition='سالم',
                                                                            unit_type='سازمان بسیج',
                                                                            Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                                   physical_condition='معاف از رزم',
                                                                                   unit_type='سازمان بسیج',
                                                                                   Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                              physical_condition='گروه ب',
                                                                              unit_type='سازمان بسیج',
                                                                              Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                                                           physical_condition='معاف+گروه ب',
                                                                                           unit_type='سازمان بسیج',
                                                                                           Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_sazman_basij = int(
        moaf_az_razm_Sufficiency_of_mobilization_sazman_basij) + int(
        groh_be_Sufficiency_of_mobilization_sazman_basij) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_sazman_basij)
    total2_Sufficiency_of_mobilization_sazman_basij = int(salem_Sufficiency_of_mobilization_sazman_basij) + int(
        moaf_az_razm_Sufficiency_of_mobilization_sazman_basij) + int(
        groh_be_Sufficiency_of_mobilization_sazman_basij) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_sazman_basij)
    total_sazman_basij = Soldier.objects.filter(has_been_accepted=True,
                                                unit_type='سازمان بسیج').all().count()
    # حوزه نمایندگی
    salem_in_course_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                              in_coures=True, physical_condition='سالم',
                                                              unit_type='حوزه نمایندگی').all().count()
    moaf_az_razm_in_course_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                                     in_coures=True, physical_condition='معاف از رزم',
                                                                     unit_type='حوزه نمایندگی').all().count()
    groh_be_in_course_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                                in_coures=True, physical_condition='گروه ب',
                                                                unit_type='حوزه نمایندگی').all().count()
    moaf_az_razm_gorh_be_in_course_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                             willing_to_learn=True,
                                                                             in_coures=True,
                                                                             physical_condition='معاف+گروه ب',
                                                                             unit_type='حوزه نمایندگی').all().count()
    total1_in_course_hoze_namayandegi = int(moaf_az_razm_in_course_hoze_namayandegi) + int(
        groh_be_in_course_hoze_namayandegi) + int(moaf_az_razm_gorh_be_in_course_hoze_namayandegi)
    total2_in_course_hoze_namayandegi = int(salem_in_course_hoze_namayandegi) + int(
        moaf_az_razm_in_course_hoze_namayandegi) + int(
        groh_be_in_course_hoze_namayandegi) + int(moaf_az_razm_gorh_be_in_course_hoze_namayandegi)

    salem_Previous_service_record_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                            physical_condition='سالم',
                                                                            unit_type='حوزه نمایندگی',
                                                                            Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                                   physical_condition='معاف از رزم',
                                                                                   unit_type='حوزه نمایندگی',
                                                                                   Previous_service_record=True).all().count()
    groh_be_Previous_service_record_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                              physical_condition='گروه ب',
                                                                              unit_type='حوزه نمایندگی',
                                                                              Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                                           physical_condition='معاف+گروه ب',
                                                                                           unit_type='حوزه نمایندگی',
                                                                                           Previous_service_record=True).all().count()
    total1_Previous_service_record_hoze_namayandegi = int(moaf_az_razm_Previous_service_record_hoze_namayandegi) + int(
        groh_be_Previous_service_record_hoze_namayandegi) + int(
        moaf_az_razm_gorh_be_Previous_service_record_hoze_namayandegi)
    total2_Previous_service_record_hoze_namayandegi = int(salem_Previous_service_record_hoze_namayandegi) + int(
        moaf_az_razm_Previous_service_record_hoze_namayandegi) + int(
        groh_be_Previous_service_record_hoze_namayandegi) + int(
        moaf_az_razm_gorh_be_Previous_service_record_hoze_namayandegi)

    salem_Sufficiency_of_mobilization_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                                physical_condition='سالم',
                                                                                unit_type='حوزه نمایندگی',
                                                                                Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                                       physical_condition='معاف از رزم',
                                                                                       unit_type='حوزه نمایندگی',
                                                                                       Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                                  physical_condition='گروه ب',
                                                                                  unit_type='حوزه نمایندگی',
                                                                                  Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                                                               physical_condition='معاف+گروه ب',
                                                                                               unit_type='حوزه نمایندگی',
                                                                                               Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_hoze_namayandegi = int(
        moaf_az_razm_Sufficiency_of_mobilization_hoze_namayandegi) + int(
        groh_be_Sufficiency_of_mobilization_hoze_namayandegi) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_hoze_namayandegi)
    total2_Sufficiency_of_mobilization_hoze_namayandegi = int(salem_Sufficiency_of_mobilization_hoze_namayandegi) + int(
        moaf_az_razm_Sufficiency_of_mobilization_hoze_namayandegi) + int(
        groh_be_Sufficiency_of_mobilization_hoze_namayandegi) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_hoze_namayandegi)
    total_hoze_namayandegi = Soldier.objects.filter(has_been_accepted=True,
                                                    unit_type='حوزه نمایندگی').all().count()
    # ستاد کل نیروهای مسلح
    salem_in_course_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                                        in_coures=True, physical_condition='سالم',
                                                                        unit_type='ستاد کل نیروهای مسلح').all().count()
    moaf_az_razm_in_course_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                                               willing_to_learn=True,
                                                                               in_coures=True,
                                                                               physical_condition='معاف از رزم',
                                                                               unit_type='ستاد کل نیروهای مسلح').all().count()
    groh_be_in_course_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                                          in_coures=True, physical_condition='گروه ب',
                                                                          unit_type='ستاد کل نیروهای مسلح').all().count()
    moaf_az_razm_gorh_be_in_course_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                                                       willing_to_learn=True,
                                                                                       in_coures=True,
                                                                                       physical_condition='معاف+گروه ب',
                                                                                       unit_type='ستاد کل نیروهای مسلح').all().count()
    total1_in_course_setad_koll_nirooye_mosalah = int(moaf_az_razm_in_course_setad_koll_nirooye_mosalah) + int(
        groh_be_in_course_setad_koll_nirooye_mosalah) + int(moaf_az_razm_gorh_be_in_course_setad_koll_nirooye_mosalah)
    total2_in_course_setad_koll_nirooye_mosalah = int(salem_in_course_setad_koll_nirooye_mosalah) + int(
        moaf_az_razm_in_course_setad_koll_nirooye_mosalah) + int(
        groh_be_in_course_setad_koll_nirooye_mosalah) + int(moaf_az_razm_gorh_be_in_course_setad_koll_nirooye_mosalah)

    salem_Previous_service_record_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                                                      physical_condition='سالم',
                                                                                      unit_type='ستاد کل نیروهای مسلح',
                                                                                      Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                                                             physical_condition='معاف از رزم',
                                                                                             unit_type='ستاد کل نیروهای مسلح',
                                                                                             Previous_service_record=True).all().count()
    groh_be_Previous_service_record_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                                                        physical_condition='گروه ب',
                                                                                        unit_type='ستاد کل نیروهای مسلح',
                                                                                        Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_setad_koll_nirooye_mosalah = Soldier.objects.filter(
        has_been_accepted=True,
        physical_condition='معاف+گروه ب',
        unit_type='ستاد کل نیروهای مسلح',
        Previous_service_record=True).all().count()
    total1_Previous_service_record_setad_koll_nirooye_mosalah = int(
        moaf_az_razm_Previous_service_record_setad_koll_nirooye_mosalah) + int(
        groh_be_Previous_service_record_setad_koll_nirooye_mosalah) + int(
        moaf_az_razm_gorh_be_Previous_service_record_setad_koll_nirooye_mosalah)
    total2_Previous_service_record_setad_koll_nirooye_mosalah = int(
        salem_Previous_service_record_setad_koll_nirooye_mosalah) + int(
        moaf_az_razm_Previous_service_record_setad_koll_nirooye_mosalah) + int(
        groh_be_Previous_service_record_setad_koll_nirooye_mosalah) + int(
        moaf_az_razm_gorh_be_Previous_service_record_setad_koll_nirooye_mosalah)

    salem_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                                                          physical_condition='سالم',
                                                                                          unit_type='ستاد کل نیروهای مسلح',
                                                                                          Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                                                                 physical_condition='معاف از رزم',
                                                                                                 unit_type='ستاد کل نیروهای مسلح',
                                                                                                 Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                                                            physical_condition='گروه ب',
                                                                                            unit_type='ستاد کل نیروهای مسلح',
                                                                                            Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah = Soldier.objects.filter(
        has_been_accepted=True,
        physical_condition='معاف+گروه ب',
        unit_type='ستاد کل نیروهای مسلح',
        Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah = int(
        moaf_az_razm_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah) + int(
        groh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah)
    total2_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah = int(
        salem_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah) + int(
        moaf_az_razm_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah) + int(
        groh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah)
    total_setad_koll_nirooye_mosalah = Soldier.objects.filter(has_been_accepted=True,
                                                              unit_type='ستاد کل نیروهای مسلح').all().count()
    # امریه دار
    salem_in_course_amire = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                   in_coures=True, physical_condition='سالم',
                                                   Amriye=True).all().count()
    moaf_az_razm_in_course_amire = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                          in_coures=True, physical_condition='معاف از رزم',
                                                          Amriye=True).all().count()
    groh_be_in_course_amire = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                     in_coures=True, physical_condition='گروه ب',
                                                     Amriye=True).all().count()
    moaf_az_razm_gorh_be_in_course_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                  willing_to_learn=True,
                                                                  in_coures=True,
                                                                  physical_condition='معاف+گروه ب',
                                                                  Amriye=True, ).all().count()
    total1_in_course_amire = int(moaf_az_razm_in_course_amire) + int(
        groh_be_in_course_amire) + int(moaf_az_razm_gorh_be_in_course_amire)
    total2_in_course_amire = int(salem_in_course_amire) + int(
        moaf_az_razm_in_course_amire) + int(
        groh_be_in_course_amire) + int(moaf_az_razm_gorh_be_in_course_amire)

    salem_Previous_service_record_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                 physical_condition='سالم',
                                                                 Amriye=True,
                                                                 Previous_service_record=True).all().count()
    moaf_az_razm_Previous_service_record_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                        physical_condition='معاف از رزم',
                                                                        Amriye=True,
                                                                        Previous_service_record=True).all().count()
    groh_be_Previous_service_record_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                   physical_condition='گروه ب',
                                                                   Amriye=True,
                                                                   Previous_service_record=True).all().count()
    moaf_az_razm_gorh_be_Previous_service_record_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                                physical_condition='معاف+گروه ب',
                                                                                Amriye=True,
                                                                                Previous_service_record=True).all().count()
    total1_Previous_service_record_amire = int(moaf_az_razm_Previous_service_record_amire) + int(
        groh_be_Previous_service_record_amire) + int(
        moaf_az_razm_gorh_be_Previous_service_record_amire)
    total2_Previous_service_record_amire = int(salem_Previous_service_record_amire) + int(
        moaf_az_razm_Previous_service_record_amire) + int(
        groh_be_Previous_service_record_amire) + int(
        moaf_az_razm_gorh_be_Previous_service_record_amire)

    salem_Sufficiency_of_mobilization_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                     physical_condition='سالم',
                                                                     Amriye=True,
                                                                     Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_Sufficiency_of_mobilization_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                            physical_condition='معاف از رزم',
                                                                            Amriye=True,
                                                                            Sufficiency_of_mobilization=True).all().count()
    groh_be_Sufficiency_of_mobilization_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                       physical_condition='گروه ب',
                                                                       Amriye=True,
                                                                       Sufficiency_of_mobilization=True).all().count()
    moaf_az_razm_gorh_be_Sufficiency_of_mobilization_amire = Soldier.objects.filter(has_been_accepted=True,
                                                                                    physical_condition='معاف+گروه ب',
                                                                                    Amriye=True,
                                                                                    Sufficiency_of_mobilization=True).all().count()
    total1_Sufficiency_of_mobilization_amire = int(
        moaf_az_razm_Sufficiency_of_mobilization_amire) + int(
        groh_be_Sufficiency_of_mobilization_amire) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_amire)
    total2_Sufficiency_of_mobilization_amire = int(salem_Sufficiency_of_mobilization_amire) + int(
        moaf_az_razm_Sufficiency_of_mobilization_amire) + int(
        groh_be_Sufficiency_of_mobilization_amire) + int(
        moaf_az_razm_gorh_be_Sufficiency_of_mobilization_amire)
    total_amire = Soldier.objects.filter(has_been_accepted=True,
                                         Amriye=True).all().count()
    barge_sazb = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True).all().count()
    kefaiti = Soldier.objects.filter(has_been_accepted=True, Sufficiency_of_mobilization=True).all().count()
    khedmat_ghabli = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True).all().count()
    kefaiti_khedmat_ghabli = int(kefaiti) + int(khedmat_ghabli)
    pazireh_shode = Soldier.objects.filter(has_been_accepted=True).all().count()
    total1 = int(salem_in_course_pa_radeh_aghmari) + int(salem_in_course_nezsa) + int(salem_in_course_neghsa) + int(
        salem_in_course_sazman_basij) + int(salem_in_course_hoze_namayandegi) + int(
        salem_in_course_setad_koll_nirooye_mosalah)
    total2 = int(total1_in_course_pa_radeh_aghmari) + int(total1_in_course_nezsa) + int(total1_in_course_neghsa) + int(
        total1_in_course_sazman_basij) + int(total1_in_course_hoze_namayandegi) + int(
        total1_in_course_setad_koll_nirooye_mosalah)
    sum1 = int(total1) + int(total2)
    total3 = int(salem_Previous_service_record_pa_radeh_aghmari) + int(salem_Previous_service_record_nezsa) + int(
        salem_Previous_service_record_neghsa) + int(
        salem_Previous_service_record_sazman_basij) + int(salem_Previous_service_record_hoze_namayandegi) + int(
        salem_Previous_service_record_setad_koll_nirooye_mosalah)
    total4 = int(total1_Previous_service_record_pa_radeh_aghmari) + int(total1_Previous_service_record_nezsa) + int(
        total1_Previous_service_record_neghsa) + int(
        total1_Previous_service_record_sazman_basij) + int(total2_Previous_service_record_hoze_namayandegi) + int(
        total1_Previous_service_record_setad_koll_nirooye_mosalah)
    sum2 = int(total3) + int(total4)
    total5 = int(salem_Sufficiency_of_mobilization_pa_radeh_aghmari) + int(
        salem_Sufficiency_of_mobilization_nezsa) + int(salem_Sufficiency_of_mobilization_neghsa) + int(
        salem_Sufficiency_of_mobilization_sazman_basij) + int(salem_Sufficiency_of_mobilization_hoze_namayandegi) + int(
        salem_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah)
    total6 = int(total1_Sufficiency_of_mobilization_pa_radeh_aghmari) + int(
        total1_Sufficiency_of_mobilization_nezsa) + int(total1_Sufficiency_of_mobilization_neghsa) + int(
        total1_Sufficiency_of_mobilization_sazman_basij) + int(
        total1_Sufficiency_of_mobilization_hoze_namayandegi) + int(
        total1_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah)
    sum3 = int(total5) + int(total6)
    t_sum = int(sum1) + int(sum2) + int(sum3)
    context = {
        'total1': total1,
        'total2': total2,
        'total3': total3,
        'total4': total4,
        'total5': total5,
        'total6': total6,
        'sum1': sum1,
        'sum2': sum2,
        'sum3': sum3,
        't_sum': t_sum,
        'pazireh_shode': pazireh_shode,
        'barge_sazb': barge_sazb,
        "kefaiti_khedmat_ghabli": kefaiti_khedmat_ghabli,
        'salem_in_course_amire': salem_in_course_amire,
        'moaf_az_razm_in_course_amire': moaf_az_razm_in_course_amire,
        'groh_be_in_course_amire': groh_be_in_course_amire,
        'moaf_az_razm_gorh_be_in_course_amire': moaf_az_razm_gorh_be_in_course_amire,
        'total1_in_course_amire': total1_in_course_amire,
        'total2_in_course_amire': total2_in_course_amire,
        'salem_Previous_service_record_amire': salem_Previous_service_record_amire,
        'moaf_az_razm_Previous_service_record_amire': moaf_az_razm_Previous_service_record_amire,
        'groh_be_Previous_service_record_amire': groh_be_Previous_service_record_amire,
        'moaf_az_razm_gorh_be_Previous_service_record_amire': moaf_az_razm_gorh_be_Previous_service_record_amire,
        'total1_Previous_service_record_amire': total1_Previous_service_record_amire,
        'total2_Previous_service_record_amire': total2_Previous_service_record_amire,
        'salem_Sufficiency_of_mobilization_amire': salem_Sufficiency_of_mobilization_amire,
        'moaf_az_razm_Sufficiency_of_mobilization_amire': moaf_az_razm_Sufficiency_of_mobilization_amire,
        'groh_be_Sufficiency_of_mobilization_amire': groh_be_Sufficiency_of_mobilization_amire,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_amire': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_amire,
        'total1_Sufficiency_of_mobilization_amire': total1_Sufficiency_of_mobilization_amire,
        'total2_Sufficiency_of_mobilization_amire': total2_Sufficiency_of_mobilization_amire,
        'total_amire': total_amire,
        'salem_in_course_pa_radeh_aghmari': salem_in_course_pa_radeh_aghmari,
        'moaf_az_razm_in_course_pa_radeh_aghmari': moaf_az_razm_in_course_pa_radeh_aghmari,
        'groh_be_in_course_pa_radeh_aghmari': groh_be_in_course_pa_radeh_aghmari,
        'moaf_az_razm_gorh_be_in_course_pa_radeh_aghmari': moaf_az_razm_gorh_be_in_course_pa_radeh_aghmari,
        'total1_in_course_pa_radeh_aghmari': total1_in_course_pa_radeh_aghmari,
        'total2_in_course_pa_radeh_aghmari': total2_in_course_pa_radeh_aghmari,
        'salem_Previous_service_record_pa_radeh_aghmari': salem_Previous_service_record_pa_radeh_aghmari,
        'moaf_az_razm_Previous_service_record_pa_radeh_aghmari': moaf_az_razm_Previous_service_record_pa_radeh_aghmari,
        'groh_be_Previous_service_record_pa_radeh_aghmari': groh_be_Previous_service_record_pa_radeh_aghmari,
        'moaf_az_razm_gorh_be_Previous_service_record_pa_radeh_aghmari': moaf_az_razm_gorh_be_Previous_service_record_pa_radeh_aghmari,
        'total1_Previous_service_record_pa_radeh_aghmari': total1_Previous_service_record_pa_radeh_aghmari,
        'total2_Previous_service_record_pa_radeh_aghmari': total2_Previous_service_record_pa_radeh_aghmari,
        'salem_Sufficiency_of_mobilization_pa_radeh_aghmari': salem_Sufficiency_of_mobilization_pa_radeh_aghmari,
        'moaf_az_razm_Sufficiency_of_mobilization_pa_radeh_aghmari': moaf_az_razm_Sufficiency_of_mobilization_pa_radeh_aghmari,
        'groh_be_Sufficiency_of_mobilization_pa_radeh_aghmari': groh_be_Sufficiency_of_mobilization_pa_radeh_aghmari,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_pa_radeh_aghmari': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_pa_radeh_aghmari,
        'total1_Sufficiency_of_mobilization_pa_radeh_aghmari': total1_Sufficiency_of_mobilization_pa_radeh_aghmari,
        'total2_Sufficiency_of_mobilization_pa_radeh_aghmari': total2_Sufficiency_of_mobilization_pa_radeh_aghmari,
        'total_pa_radeh_aghmari': total_pa_radeh_aghmari,
        'salem_in_course_nezsa': salem_in_course_nezsa,
        'moaf_az_razm_in_course_nezsa': moaf_az_razm_in_course_nezsa,
        'groh_be_in_course_nezsa': groh_be_in_course_nezsa,
        'moaf_az_razm_gorh_be_in_course_nezsa': moaf_az_razm_gorh_be_in_course_nezsa,
        'total1_in_course_nezsa': total1_in_course_nezsa,
        'total2_in_course_nezsa': total2_in_course_nezsa,
        'salem_Previous_service_record_nezsa': salem_Previous_service_record_nezsa,
        'moaf_az_razm_Previous_service_record_nezsa': moaf_az_razm_Previous_service_record_nezsa,
        'groh_be_Previous_service_record_nezsa': groh_be_Previous_service_record_nezsa,
        'moaf_az_razm_gorh_be_Previous_service_record_nezsa': moaf_az_razm_gorh_be_Previous_service_record_nezsa,
        'total1_Previous_service_record_nezsa': total1_Previous_service_record_nezsa,
        'total2_Previous_service_record_nezsa': total2_Previous_service_record_nezsa,
        'salem_Sufficiency_of_mobilization_nezsa': salem_Sufficiency_of_mobilization_nezsa,
        'moaf_az_razm_Sufficiency_of_mobilization_nezsa': moaf_az_razm_Sufficiency_of_mobilization_nezsa,
        'groh_be_Sufficiency_of_mobilization_nezsa': groh_be_Sufficiency_of_mobilization_nezsa,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_nezsa': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_nezsa,
        'total1_Sufficiency_of_mobilization_nezsa': total1_Sufficiency_of_mobilization_nezsa,
        'total2_Sufficiency_of_mobilization_nezsa': total2_Sufficiency_of_mobilization_nezsa,
        'total_nezsa': total_nezsa,
        'salem_in_course_neghsa': salem_in_course_neghsa,
        'moaf_az_razm_in_course_neghsa': moaf_az_razm_in_course_neghsa,
        'groh_be_in_course_neghsa': groh_be_in_course_neghsa,
        'moaf_az_razm_gorh_be_in_course_neghsa': moaf_az_razm_gorh_be_in_course_neghsa,
        'total1_in_course_neghsa': total1_in_course_neghsa,
        'total2_in_course_neghsa': total2_in_course_neghsa,
        'salem_Previous_service_record_neghsa': salem_Previous_service_record_neghsa,
        'moaf_az_razm_Previous_service_record_neghsa': moaf_az_razm_Previous_service_record_neghsa,
        'groh_be_Previous_service_record_neghsa': groh_be_Previous_service_record_neghsa,
        'moaf_az_razm_gorh_be_Previous_service_record_neghsa': moaf_az_razm_gorh_be_Previous_service_record_neghsa,
        'total1_Previous_service_record_neghsa': total1_Previous_service_record_neghsa,
        'total2_Previous_service_record_neghsa': total2_Previous_service_record_neghsa,
        'salem_Sufficiency_of_mobilization_neghsa': salem_Sufficiency_of_mobilization_neghsa,
        'moaf_az_razm_Sufficiency_of_mobilization_neghsa': moaf_az_razm_Sufficiency_of_mobilization_neghsa,
        'groh_be_Sufficiency_of_mobilization_neghsa': groh_be_Sufficiency_of_mobilization_neghsa,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_neghsa': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_neghsa,
        'total1_Sufficiency_of_mobilization_neghsa': total1_Sufficiency_of_mobilization_neghsa,
        'total2_Sufficiency_of_mobilization_neghsa': total2_Sufficiency_of_mobilization_neghsa,
        'total_neghsa': total_neghsa,
        'salem_in_course_ndsa': salem_in_course_ndsa,
        'moaf_az_razm_in_course_ndsa': moaf_az_razm_in_course_ndsa,
        'groh_be_in_course_ndsa': groh_be_in_course_ndsa,
        'moaf_az_razm_gorh_be_in_course_ndsa': moaf_az_razm_gorh_be_in_course_ndsa,
        'total1_in_course_ndsa': total1_in_course_ndsa,
        'total2_in_course_ndsa': total2_in_course_ndsa,
        'salem_Previous_service_record_ndsa': salem_Previous_service_record_ndsa,
        'moaf_az_razm_Previous_service_record_ndsa': moaf_az_razm_Previous_service_record_ndsa,
        'groh_be_Previous_service_record_ndsa': groh_be_Previous_service_record_ndsa,
        'moaf_az_razm_gorh_be_Previous_service_record_ndsa': moaf_az_razm_gorh_be_Previous_service_record_ndsa,
        'total1_Previous_service_record_ndsa': total1_Previous_service_record_ndsa,
        'total2_Previous_service_record_ndsa': total2_Previous_service_record_ndsa,
        'salem_Sufficiency_of_mobilization_ndsa': salem_Sufficiency_of_mobilization_ndsa,
        'moaf_az_razm_Sufficiency_of_mobilization_ndsa': moaf_az_razm_Sufficiency_of_mobilization_ndsa,
        'groh_be_Sufficiency_of_mobilization_ndsa': groh_be_Sufficiency_of_mobilization_ndsa,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_ndsa': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_ndsa,
        'total1_Sufficiency_of_mobilization_ndsa': total1_Sufficiency_of_mobilization_ndsa,
        'total2_Sufficiency_of_mobilization_ndsa': total2_Sufficiency_of_mobilization_ndsa,
        'total_ndsa': total_ndsa,
        'salem_in_course_havafaza': salem_in_course_havafaza,
        'moaf_az_razm_in_course_havafaza': moaf_az_razm_in_course_havafaza,
        'groh_be_in_course_havafaza': groh_be_in_course_havafaza,
        'moaf_az_razm_gorh_be_in_course_havafaza': moaf_az_razm_gorh_be_in_course_havafaza,
        'total1_in_course_havafaza': total1_in_course_havafaza,
        'total2_in_course_havafaza': total2_in_course_havafaza,
        'salem_Previous_service_record_havafaza': salem_Previous_service_record_havafaza,
        'moaf_az_razm_Previous_service_record_havafaza': moaf_az_razm_Previous_service_record_havafaza,
        'groh_be_Previous_service_record_havafaza': groh_be_Previous_service_record_havafaza,
        'moaf_az_razm_gorh_be_Previous_service_record_havafaza': moaf_az_razm_gorh_be_Previous_service_record_havafaza,
        'total1_Previous_service_record_havafaza': total1_Previous_service_record_havafaza,
        'total2_Previous_service_record_havafaza': total2_Previous_service_record_havafaza,
        'salem_Sufficiency_of_mobilization_havafaza': salem_Sufficiency_of_mobilization_havafaza,
        'moaf_az_razm_Sufficiency_of_mobilization_havafaza': moaf_az_razm_Sufficiency_of_mobilization_havafaza,
        'groh_be_Sufficiency_of_mobilization_havafaza': groh_be_Sufficiency_of_mobilization_havafaza,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_havafaza': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_havafaza,
        'total1_Sufficiency_of_mobilization_havafaza': total1_Sufficiency_of_mobilization_havafaza,
        'total2_Sufficiency_of_mobilization_havafaza': total2_Sufficiency_of_mobilization_havafaza,
        'total_havafaza': total_havafaza,
        'salem_in_course_sazman_basij': salem_in_course_sazman_basij,
        'moaf_az_razm_in_course_sazman_basij': moaf_az_razm_in_course_sazman_basij,
        'groh_be_in_course_sazman_basij': groh_be_in_course_sazman_basij,
        'moaf_az_razm_gorh_be_in_course_sazman_basij': moaf_az_razm_gorh_be_in_course_sazman_basij,
        'total1_in_course_sazman_basij': total1_in_course_sazman_basij,
        'total2_in_course_sazman_basij': total2_in_course_sazman_basij,
        'salem_Previous_service_record_sazman_basij': salem_Previous_service_record_sazman_basij,
        'moaf_az_razm_Previous_service_record_sazman_basij': moaf_az_razm_Previous_service_record_sazman_basij,
        'groh_be_Previous_service_record_sazman_basij': groh_be_Previous_service_record_sazman_basij,
        'moaf_az_razm_gorh_be_Previous_service_record_sazman_basij': moaf_az_razm_gorh_be_Previous_service_record_sazman_basij,
        'total1_Previous_service_record_sazman_basij': total1_Previous_service_record_sazman_basij,
        'total2_Previous_service_record_sazman_basij': total2_Previous_service_record_sazman_basij,
        'salem_Sufficiency_of_mobilization_sazman_basij': salem_Sufficiency_of_mobilization_sazman_basij,
        'moaf_az_razm_Sufficiency_of_mobilization_sazman_basij': moaf_az_razm_Sufficiency_of_mobilization_sazman_basij,
        'groh_be_Sufficiency_of_mobilization_sazman_basij': groh_be_Sufficiency_of_mobilization_sazman_basij,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_sazman_basij': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_sazman_basij,
        'total1_Sufficiency_of_mobilization_sazman_basij': total1_Sufficiency_of_mobilization_sazman_basij,
        'total2_Sufficiency_of_mobilization_sazman_basij': total2_Sufficiency_of_mobilization_sazman_basij,
        'total_sazman_basij': total_sazman_basij,
        'salem_in_course_hoze_namayandegi': salem_in_course_hoze_namayandegi,
        'moaf_az_razm_in_course_hoze_namayandegi': moaf_az_razm_in_course_hoze_namayandegi,
        'groh_be_in_course_hoze_namayandegi': groh_be_in_course_hoze_namayandegi,
        'moaf_az_razm_gorh_be_in_course_hoze_namayandegi': moaf_az_razm_gorh_be_in_course_hoze_namayandegi,
        'total1_in_course_hoze_namayandegi': total1_in_course_hoze_namayandegi,
        'total2_in_course_hoze_namayandegi': total2_in_course_hoze_namayandegi,
        'salem_Previous_service_record_hoze_namayandegi': salem_Previous_service_record_hoze_namayandegi,
        'moaf_az_razm_Previous_service_record_hoze_namayandegi': moaf_az_razm_Previous_service_record_hoze_namayandegi,
        'groh_be_Previous_service_record_hoze_namayandegi': groh_be_Previous_service_record_hoze_namayandegi,
        'moaf_az_razm_gorh_be_Previous_service_record_hoze_namayandegi': moaf_az_razm_gorh_be_Previous_service_record_hoze_namayandegi,
        'total1_Previous_service_record_hoze_namayandegi': total1_Previous_service_record_hoze_namayandegi,
        'total2_Previous_service_record_hoze_namayandegi': total2_Previous_service_record_hoze_namayandegi,
        'salem_Sufficiency_of_mobilization_hoze_namayandegi': salem_Sufficiency_of_mobilization_hoze_namayandegi,
        'moaf_az_razm_Sufficiency_of_mobilization_hoze_namayandegi': moaf_az_razm_Sufficiency_of_mobilization_hoze_namayandegi,
        'groh_be_Sufficiency_of_mobilization_hoze_namayandegi': groh_be_Sufficiency_of_mobilization_hoze_namayandegi,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_hoze_namayandegi': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_hoze_namayandegi,
        'total1_Sufficiency_of_mobilization_hoze_namayandegi': total1_Sufficiency_of_mobilization_hoze_namayandegi,
        'total2_Sufficiency_of_mobilization_hoze_namayandegi': total2_Sufficiency_of_mobilization_hoze_namayandegi,
        'total_hoze_namayandegi': total_hoze_namayandegi,
        'salem_in_course_setad_koll_nirooye_mosalah': salem_in_course_setad_koll_nirooye_mosalah,
        'moaf_az_razm_in_course_setad_koll_nirooye_mosalah': moaf_az_razm_in_course_setad_koll_nirooye_mosalah,
        'groh_be_in_course_setad_koll_nirooye_mosalah': groh_be_in_course_setad_koll_nirooye_mosalah,
        'moaf_az_razm_gorh_be_in_course_setad_koll_nirooye_mosalah': moaf_az_razm_gorh_be_in_course_setad_koll_nirooye_mosalah,
        'total1_in_course_setad_koll_nirooye_mosalah': total1_in_course_setad_koll_nirooye_mosalah,
        'total2_in_course_setad_koll_nirooye_mosalah': total2_in_course_setad_koll_nirooye_mosalah,
        'salem_Previous_service_record_setad_koll_nirooye_mosalah': salem_Previous_service_record_setad_koll_nirooye_mosalah,
        'moaf_az_razm_Previous_service_record_setad_koll_nirooye_mosalah': moaf_az_razm_Previous_service_record_setad_koll_nirooye_mosalah,
        'groh_be_Previous_service_record_setad_koll_nirooye_mosalah': groh_be_Previous_service_record_setad_koll_nirooye_mosalah,
        'moaf_az_razm_gorh_be_Previous_service_record_setad_koll_nirooye_mosalah': moaf_az_razm_gorh_be_Previous_service_record_setad_koll_nirooye_mosalah,
        'total1_Previous_service_record_setad_koll_nirooye_mosalah': total1_Previous_service_record_setad_koll_nirooye_mosalah,
        'total2_Previous_service_record_setad_koll_nirooye_mosalah': total2_Previous_service_record_setad_koll_nirooye_mosalah,
        'salem_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah': salem_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah,
        'moaf_az_razm_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah': moaf_az_razm_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah,
        'groh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah': groh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah,
        'moaf_az_razm_gorh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah': moaf_az_razm_gorh_be_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah,
        'total1_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah': total1_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah,
        'total2_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah': total2_Sufficiency_of_mobilization_setad_koll_nirooye_mosalah,
        'total_setad_koll_nirooye_mosalah': total_setad_koll_nirooye_mosalah,
    }
    return render(request, 'ensani_statistics/amar_yegan_be_kar_girande_tabel.html', context)


@login_required
def gozaresh_payan_dore(request):
    amare_paziresh_shode = Soldier.objects.filter(has_been_accepted=True).all().count()
    salem = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                   physical_condition='سالم',
                                   Sufficiency_of_mobilization=False, Amriye=False,
                                   Previous_service_record=False).all().count()
    moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='معاف از رزم',
                                          Sufficiency_of_mobilization=False, Amriye=False,
                                          Previous_service_record=False).all().count()
    gore_be = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='گروه ب',
                                     Sufficiency_of_mobilization=False, Amriye=False,
                                     Previous_service_record=False).all().count()
    gore_be_moafezrazm = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                physical_condition='معاف+گروه ب',
                                                Sufficiency_of_mobilization=False, Amriye=False,
                                                Previous_service_record=False).all().count()
    Sufficiency_of_mobilization = Soldier.objects.filter(has_been_accepted=True,
                                                         Sufficiency_of_mobilization=True, Amriye=False).all().count()
    Previous_service_record = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True,
                                                     Sufficiency_of_mobilization=False, Amriye=False).all().count()
    comision_shoro_dore = NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی",
                                                            soldire__the_medical_commission=True,
                                                            soldire__Amriye=False).all().count()
    total_1 = int(salem) + int(moaf_az_razm) + int(gore_be) + int(gore_be_moafezrazm) + int(
        Sufficiency_of_mobilization) + int(comision_shoro_dore) + int(
        Previous_service_record)
    total_2 = int(Sufficiency_of_mobilization) + int(comision_shoro_dore) + int(Previous_service_record)

    a_salem = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='سالم',
                                     Sufficiency_of_mobilization=False, Amriye=True,
                                     Previous_service_record=False).all().count()
    a_moaf_az_razm = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='معاف از رزم',
                                            Sufficiency_of_mobilization=False, Amriye=True,
                                            Previous_service_record=False).all().count()
    a_gorh_be = Soldier.objects.filter(has_been_accepted=True, in_coures=True, physical_condition='گروه ب',
                                       Sufficiency_of_mobilization=False, Amriye=True,
                                       Previous_service_record=False).all().count()
    a_goreh_be_moh_az_razm = Soldier.objects.filter(has_been_accepted=True, in_coures=True,
                                                    physical_condition='معاف+گروه ب',
                                                    Sufficiency_of_mobilization=False, Amriye=True,
                                                    Previous_service_record=False).all().count()
    a_Sufficiency_of_mobilization = Soldier.objects.filter(has_been_accepted=True,
                                                           Sufficiency_of_mobilization=True, Amriye=True).all().count()
    a_Previous_service_record = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True,
                                                       Sufficiency_of_mobilization=False, Amriye=True).all().count()
    a_comision_shoro_dore = NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی",
                                                              soldire__the_medical_commission=True,
                                                              soldire__Amriye=True).all().count()
    a_total_1 = int(a_salem) + int(a_moaf_az_razm) + int(a_gorh_be) + int(
        a_goreh_be_moh_az_razm) + int(a_Sufficiency_of_mobilization) + int(
        a_comision_shoro_dore) + int(
        a_Previous_service_record)
    a_total_2 = int(a_Sufficiency_of_mobilization) + int(a_comision_shoro_dore) + int(a_Previous_service_record)
    total_kaheshi = a_total_2 + total_2
    shor_dore = (a_total_1 + total_1) - (total_2 + a_total_2)
    a_zire_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='زیر دیپلم').count()
    a_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='دیپلم').count()
    a_fogh_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='فوق دیپلم').count()
    a_lisans = Soldier.objects.filter(has_been_accepted=True, Grade_precise='لیسانس').count()
    a_fogh_lisans = Soldier.objects.filter(has_been_accepted=True, Grade_precise='فوق لیسانس').count()
    a_doctora = Soldier.objects.filter(has_been_accepted=True, Grade_precise='دکتری').count()
    a_bisavad = Soldier.objects.filter(has_been_accepted=True, Grade_precise='بی‌سواد').count()
    a_nehzad = Soldier.objects.filter(has_been_accepted=True, Grade_precise='نهضت سواد آموزی').count()
    a_rahinami = Soldier.objects.filter(has_been_accepted=True, Grade_precise='راهنمایی').count()
    a_sikel = Soldier.objects.filter(has_been_accepted=True, Grade_precise='سیکل').count()
    a_dabirestan = Soldier.objects.filter(has_been_accepted=True, Grade_precise='دبیرستان').count()
    a_ebtedai = Soldier.objects.filter(has_been_accepted=True, Grade_precise='ابتدایی').count()
    a_total = int(a_zire_diplom) + int(a_diplom) + int(a_fogh_diplom) + int(a_lisans) + int(a_fogh_lisans) + int(
        a_doctora) + int(a_bisavad) + int(a_nehzad) + int(a_rahinami) + int(a_sikel) + int(a_dabirestan) + int(
        a_ebtedai)
    in_course_zire_diplom = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                                   Grade_precise='زیر دیپلم').count()
    in_course_diplom = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                              Grade_precise='دیپلم').count()
    in_course_fogh_diplom = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                                   Grade_precise='فوق دیپلم').count()
    in_course_lisans = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                              Grade_precise='لیسانس').count()
    in_course_fogh_lisans = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                                   Grade_precise='فوق لیسانس').count()
    in_course_doctora = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                               Grade_precise='دکتری').count()
    in_course_bisavad = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                               Grade_precise='بی‌سواد').count()
    in_course_nehzad = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                              Grade_precise='نهضت سواد آموزی').count()
    in_course_rahinami = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                                Grade_precise='راهنمایی').count()
    in_course_sikel = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                             Grade_precise='سیکل').count()
    in_course_dabirestan = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                                  Grade_precise='دبیرستان').count()
    in_course_ebtedai = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True,
                                               Grade_precise='ابتدایی').count()

    in_courese_total = int(in_course_zire_diplom) + int(in_course_diplom) + int(in_course_fogh_diplom) + int(
        in_course_lisans) + int(in_course_fogh_lisans) + int(in_course_doctora) + int(
        in_course_bisavad) + int(in_course_nehzad) + int(in_course_rahinami) + int(in_course_sikel) + int(
        in_course_dabirestan) + int(in_course_ebtedai)
    en = EnsaniSettings.objects.filter().first()
    cx = {

        'salem': salem,
        'moaf_az_razm': moaf_az_razm,
        'amare_paziresh_shode': amare_paziresh_shode,
        'Sufficiency_of_mobilization': Sufficiency_of_mobilization,
        'Previous_service_record': Previous_service_record,
        'comision_shoro_dore': comision_shoro_dore,
        'total_1': total_1,
        'total_2': total_2,
        'asalem': a_salem,
        'amoaf_az_razm': a_moaf_az_razm,
        'gore_be': gore_be,
        'a_gorh_be': a_gorh_be,
        'a_goreh_be_moh_az_razm': a_goreh_be_moh_az_razm,
        'aSufficiency_of_mobilization': a_Sufficiency_of_mobilization,
        'aPrevious_service_record': a_Previous_service_record,
        'acomision_shoro_dore': a_comision_shoro_dore,
        'atotal_1': a_total_1,
        'atotal_2': a_total_2,
        'total_kaheshi': total_kaheshi,
        'shor_dore': shor_dore,
        'a_zire_diplom': a_zire_diplom,
        'a_diplom': a_diplom,
        'a_fogh_diplom': a_fogh_diplom,
        'a_lisans': a_lisans,
        'a_fogh_lisans': a_fogh_lisans,
        'a_doctora': a_doctora,
        'a_bisavad': a_bisavad + a_zire_diplom,
        'a_nehzad': a_nehzad,
        'a_rahinami': a_rahinami,
        'a_sikel': a_sikel,
        'a_dabirestan': a_dabirestan,
        'a_ebtedai': a_ebtedai,
        'a_total': a_total,
        'in_course_zire_diplom': in_course_zire_diplom,
        'in_course_diplom': in_course_diplom,
        'in_course_fogh_diplom': in_course_fogh_diplom,
        'in_course_lisans': in_course_lisans,
        'in_course_fogh_lisans': in_course_fogh_lisans,
        'in_course_doctora': in_course_doctora,
        'in_course_bisavad': in_course_bisavad + in_course_zire_diplom,
        'in_course_nehzad': in_course_nehzad,
        'in_course_rahinami': in_course_rahinami,
        'in_course_sikel': in_course_sikel,
        'in_course_dabirestan': in_course_dabirestan,
        'in_course_ebtedai': in_course_ebtedai,
        'in_courese_total': in_courese_total,
        'en': en,

    }
    return render(request, 'ensani_statistics/gozaresh_payan_dore.html', cx)


@login_required
def amar_rank(request):
    rank_1 = Soldier.objects.filter(rank="سرباز").all().count()
    rank_2 = Soldier.objects.filter(rank="سرباز دوم").all().count()
    rank_3 = Soldier.objects.filter(rank="سرباز یکم").all().count()
    rank_4 = Soldier.objects.filter(rank="رزمیار").all().count()
    rank_5 = Soldier.objects.filter(rank="رزم‌آور سوم").all().count()
    rank_6 = Soldier.objects.filter(rank="رزم‌آور دوم").all().count()
    rank_7 = Soldier.objects.filter(rank="رزم‌آور یکم").all().count()
    rank_8 = Soldier.objects.filter(rank="رزمدار دوم").all().count()
    rank_9 = Soldier.objects.filter(rank="رزمدار یکم").all().count()
    rank_10 = Soldier.objects.filter(rank="ستوان سوم").all().count()
    rank_11 = Soldier.objects.filter(rank="ستوان دوم").all().count()
    rank_12 = Soldier.objects.filter(rank="ستوان یکم").all().count()
    total = rank_1 + rank_2 + rank_3 + rank_4 + rank_5 + rank_6 + rank_7 + rank_8 + rank_9 + rank_10 + rank_11 + rank_12
    cx = {
        'rank_1': rank_1,
        'rank_2': rank_2,
        'rank_3': rank_3,
        'rank_4': rank_4,
        'rank_5': rank_5,
        'rank_6': rank_6,
        'rank_7': rank_7,
        'rank_8': rank_8,
        'rank_9': rank_9,
        'rank_10': rank_10,
        'rank_11': rank_11,
        'rank_12': rank_12,
        'total': total,
    }
    return render(request, 'ensani_statistics/amar_rank.html', cx)
