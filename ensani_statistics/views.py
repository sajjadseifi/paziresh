from django.shortcuts import render, HttpResponse
from soldiers.models import Soldier
from django.db.models import Count, Case, When
from battalions.models import battalion, battalion_group
from ensani_letter.models import NormalLetterModels
from ensaniapp_settings.models import EnsaniSettings


# Create your views here.


def amar_avalie(request):
    settings = EnsaniSettings.objects.filter().first()
    if settings is None:
        return HttpResponse("تنظیمات دوره انجام نشده!")
    statistics = []

    if settings.tatbigh == False:
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
            'en': settings
        }

        return render(request, 'ensani_statistics/vaziate_avalie.html', context)


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


def amar_be_tafkik_madrk_tahsili(request):
    return render(request, 'ensani_statistics/amar_be_tafkik_madrak_tahsili.html')


def gozaresh_shoro_dore(request):
    amare_paziresh_shode = Soldier.objects.filter(has_been_accepted=True).all().count()
    salem = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True, in_coures=True,
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
    a_zire_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='زیر دیپلم').count()
    a_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='دیپلم').count()
    a_fogh_diplom = Soldier.objects.filter(has_been_accepted=True, Grade_precise='فوق دیپلم').count()
    a_lisans = Soldier.objects.filter(has_been_accepted=True, Grade_precise='لیسانس').count()
    a_fogh_lisans = Soldier.objects.filter(has_been_accepted=True, Grade_precise='فوق لیسانس').count()
    a_doctora = Soldier.objects.filter(has_been_accepted=True, Grade_precise='دکتری').count()
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
        'in_course_zire_diplom': in_course_zire_diplom,
        'in_course_diplom': in_course_diplom,
        'in_course_fogh_diplom': in_course_fogh_diplom,
        'in_course_lisans': in_course_lisans,
        'in_course_fogh_lisans': in_course_fogh_lisans,
        'in_course_doctora': in_course_doctora

    }
    return render(request, 'ensani_statistics/gozaresh_shoro_dore.html', cx)


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


def yegan_be_kar_girande(request):
    return render(request, 'ensani_statistics/gozaresh_yeghan_be_kar_girande.html')


def yegan_be_kar_girande_tabel(request):
    return render(request, 'ensani_statistics/amar_yegan_be_kar_girande_tabel.html')
