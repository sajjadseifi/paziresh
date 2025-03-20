a_soldire_total_shie = Soldier.objects.filter(date_improt_type='سامانه', Religion='شیعه',
                                              physical_condition='سالم', has_been_accepted=False).all().count()
a_soldire_total_tasanon = Soldier.objects.filter(date_improt_type='سامانه', Religion='اهل تسنن',
                                                 physical_condition='سالم', has_been_accepted=False).all().count()
a_soldire_total_amire = Soldier.objects.filter(date_improt_type='سامانه', Amriye=True,
                                               physical_condition='سالم', has_been_accepted=False).all().count()
a_zire_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='زیر دیپلم',
                                       physical_condition='سالم', has_been_accepted=False).count()
a_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='دیپلم', physical_condition='سالم',
                                  has_been_accepted=False).count()
a_fogh_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق دیپلم',
                                       physical_condition='سالم', has_been_accepted=False).count()
a_lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='لیسانس', physical_condition='سالم',
                                  has_been_accepted=False).count()
a_fogh_lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق لیسانس',
                                       physical_condition='سالم', has_been_accepted=False).count()
a_doctora = Soldier.objects.filter(date_improt_type='سامانه', Grade='دکتری', physical_condition='سالم',
                                   has_been_accepted=False).count()
a_namoshakhas = Soldier.objects.filter(date_improt_type='سامانه', Grade='نامشخص', physical_condition='سالم',
                                       has_been_accepted=False).count()

m_soldire_total_shie = Soldier.objects.filter(date_improt_type='سامانه', Religion='شیعه',
                                              physical_condition='معاف از رزم',
                                              has_been_accepted=False).all().count()
m_soldire_total_tasanon = Soldier.objects.filter(date_improt_type='سامانه', Religion='اهل تسنن',
                                                 physical_condition='معاف از رزم',
                                                 has_been_accepted=False).all().count()
m_soldire_total_amire = Soldier.objects.filter(date_improt_type='سامانه', Amriye=True,
                                               physical_condition='معاف از رزم',
                                               has_been_accepted=False).all().count()
m_zire_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='زیر دیپلم',
                                       physical_condition='معاف از رزم', has_been_accepted=False).count()
m_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='دیپلم',
                                  physical_condition='معاف از رزم', has_been_accepted=False).count()
m_fogh_diplom = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق دیپلم',
                                       physical_condition='معاف از رزم', has_been_accepted=False).count()
m_lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='لیسانس',
                                  physical_condition='معاف از رزم', has_been_accepted=False).count()
m_fogh_lisans = Soldier.objects.filter(date_improt_type='سامانه', Grade='فوق لیسانس',
                                       physical_condition='معاف از رزم', has_been_accepted=False).count()
m_doctora = Soldier.objects.filter(date_improt_type='سامانه', Grade='دکتری',
                                   physical_condition='معاف از رزم', has_been_accepted=False).count()
m_namoshakhas = Soldier.objects.filter(date_improt_type='سامانه', Grade='نامشخص',
                                       physical_condition='معاف از رزم', has_been_accepted=False).count()
a_goli_t = Soldier.objects.filter(date_improt_type='سامانه', physical_condition='سالم',
                                  has_been_accepted=False).count()
m_goli_t = Soldier.objects.filter(date_improt_type='سامانه', physical_condition='معاف از رزم',
                                  has_been_accepted=False).count()