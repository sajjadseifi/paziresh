from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from soldiers.models import Soldier
from battalions.models import battalion, battalion_group
from ensaniapp_settings.models import EnsaniSettings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ensani.excel_utils  import export_soldiers_to_excel,export_kafiat_to_excel   
from ensani_letter.models import NormalLetterModels,CheckoutLetterModels
from django.utils import timezone
from .models import ActivityLog
from .services.statistics import get_paziresh_peak_multi_day
class panel_home(LoginRequiredMixin, View):
    def get(self, request):
        soldire = Soldier.objects.filter().all()
        amar_kol = soldire.count()
        amar_kole_hezer_bekhdmat = soldire.filter(willing_to_learn=True).all().count()
        amar_shoro_dore = soldire.filter(has_been_accepted=True, in_coures=True).all().count()
        amar_kole_paziresh_shode = Soldier.objects.filter(has_been_accepted=True).all().count()
        tatbikh_nashode = amar_shoro_dore
        # tatbikh_nashode = Soldier.objects.filter(has_been_accepted=True, in_coures=True, the_medical_commission=False,
        #                                          Previous_service_record=False, Sufficiency_of_mobilization=False,
        #                                          tatbigh=False, IsCheckout=False).all().count()
        total_tegan_khdmati_in_course = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                               in_coures=True, IsCheckout=False,IsUnit=True).all().count()
        en = EnsaniSettings.objects.filter().first()
        b_soldire = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True).all()
        basij = Soldier.objects.filter(has_been_accepted=True,Sufficiency_of_mobilization=True).all().count()
        previous = Soldier.objects.filter(has_been_accepted=True, Previous_service_record=True).all().count()
        shoro_komisyon = NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی",soldire__the_medical_commission=True).all().count()
        komisyon = NormalLetterModels.objects.filter(subject="معرفی به کمیسیون",soldire__the_medical_commission=True).all().count()
        tajdiddoreh = CheckoutLetterModels.objects.filter(c_type="تجدید دوره").all().count()

        gsforg =Soldier.objects.filter(garargah_sazandegi_khatam=True)
        garargah_sazandegi_khatam = {
            'all':gsforg.all().count(),
            'paziresh':gsforg.filter(has_been_accepted=True).all().count(),
            'present':gsforg.filter(has_been_accepted=True,in_coures=True).all().count(),
            'shoro_komisyon' : NormalLetterModels.objects.filter(subject="معرفی به کمیسیون شروع دوره آموزشی",soldire__the_medical_commission=True,soldire__garargah_sazandegi_khatam=True).all().count(),
            'komisyon' : NormalLetterModels.objects.filter(subject="معرفی به کمیسیون",soldire__the_medical_commission=True,soldire__garargah_sazandegi_khatam=True).all().count(),
            'tajdiddoreh' : CheckoutLetterModels.objects.filter(c_type="تجدید دوره",soldire__garargah_sazandegi_khatam=True).all().count()
        }
        
        present_in_course =Soldier.objects.filter(has_been_accepted=True,in_coures=True)
        # organs  = {
        #     'amriye' :present_in_course.filter(Amriye=True).count(),
        #     'normal' :present_in_course.filter(Amriye=False,garargah_sazandegi_khatam=False).count(),
        #     'khatam' :"-",
        #     'garargah_sazandegi_khatam' :present_in_course.filter(garargah_sazandegi_khatam=True).count(),
        # }
        organs = []
        for stype in Soldier.status_types_list():
            scount = Soldier.objects.filter(status_type=stype,has_been_accepted=True,in_coures=True).count()
            organs.append({ 'label':stype, 'value':scount })
        
        list_btn = []
        name_list = []
        total_list = []
        gordan = battalion.objects.filter().all().order_by('name')
        for iteam in gordan:
            gorhan = battalion_group.objects.filter(gordan=iteam).order_by('name')
            tt = b_soldire.filter(Gordan=iteam).all().count()
            t_g = b_soldire.filter(t_Gordan=iteam).all().count()
            
            if tt != 0 or t_g != 0:
                total_list.append(tt)
                name_list.append(iteam.name)
            for iteam in gorhan:
                t = b_soldire.filter(battalion_group=iteam).all().count()
                t_t = b_soldire.filter(t_battalion_group=iteam).all().count()
                t_tn = b_soldire.filter(battalion_group=iteam,t_battalion_group=None).all().count()
                if t != 0:
                    list_btn.append({
                        'gordan': iteam.gordan.name, 
                        'gorohan': iteam.name, 
                        'count': t,
                        't_count': t_t,
                        'tn_count': t_tn,
                    })
        if len(list_btn) > 1:
            gordan = 'مجموع' 
            gorohan = len(list_btn) 
            count    = sum(lb['count'] for lb in list_btn)
            t_count  = sum(lb['t_count'] for lb in list_btn)
            tn_count = sum(lb['tn_count'] for lb in list_btn)
            tatbikh_nashode =  tn_count
            list_btn.append({
                'class':'total-row', 
                'gordan': gordan,  
                'gorohan': gorohan,  
                'count': count, 
                't_count': t_count,
                'tn_count': tn_count,
            })
        today = timezone.localtime(timezone.now()).date()
        logs_today = ActivityLog.objects.filter(created_at__date=today).count()
        
        en = EnsaniSettings.objects.first()
        peakChart = get_paziresh_peak_multi_day(en.tarikhpaziresh ,en.tarikhetmampaziresh)
        cx = {
            'peakChart':peakChart,
            'logs_today': logs_today,
            'amar_kol': amar_kol, 
            'amar_kole_hezer_bekhdmat': amar_kole_hezer_bekhdmat,
            'amar_kole_paziresh_shode': amar_kole_paziresh_shode, 'tatbikh_nashode': tatbikh_nashode,
            'total_tegan_khdmati_in_course': total_tegan_khdmati_in_course, 'list_btn': list_btn,
            'name_list': name_list, 
            'total_list': total_list,
            'amar_shoro_dore':amar_shoro_dore,
            'basij':basij ,  # مثال
            'komisyon': komisyon,
            'shoro_komisyon':shoro_komisyon ,
            'previous':previous ,
            'tajdiddoreh':tajdiddoreh,
            'organs':organs,
            'garargah_sazandegi_khatam':garargah_sazandegi_khatam
        }
        return render(request, 'ensani/panel_home_page.html', cx)

@login_required
def support(request, *args, **kwargs):
    return render(request, 'ensani/poshtibani.html')


# Create your views here.
def header_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Header.html')


def header_references_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_HeaderReferences.html')


def navbar_partial_view(request, *args, **kwargs):
    user = request.user.is_staff == True
    return render(request, 'shared/_Navbar.html')


def footer_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Footer.html')


def footer_references_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_FooterReferences.html')


def get_excel_response(df, filename):
    """Convert DataFrame to Excel and return as response."""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
    df.to_excel(response, index=False)
    return response


def download_amar_kol(request):
    return export_soldiers_to_excel(filename='amar_kol')

def download_shoro_dore(request):
    return export_soldiers_to_excel(
        filter_kwargs={'has_been_accepted': True, 'in_coures': True},
        filename='shoro_dore'
    )

def download_hezer(request):
    return export_soldiers_to_excel(
        filter_kwargs={'has_been_accepted': True, 'willing_to_learn': True, 'in_coures': True},
        filename='hezer'
    )

def download_paziresh(request):
    return export_soldiers_to_excel(
        filter_kwargs={'has_been_accepted': True},
        filename='paziresh'
    )

def download_yegan(request):
    return export_soldiers_to_excel(
        filter_kwargs={'has_been_accepted': True, 'willing_to_learn': True, 'in_coures': True, 'IsCheckout': False, 'IsUnit': False},
        filename='yegan'
    )

def download_tatbikh(request):
    return export_soldiers_to_excel(
        filter_kwargs={
            'has_been_accepted': True, 'in_coures': True,
            'the_medical_commission': False,
            'Previous_service_record': False,
            'Sufficiency_of_mobilization': False,
            'tatbigh': False,
            'IsCheckout': False
        },
        filename='tatbikh'
    )

def download_kafiat(request):
    return export_kafiat_to_excel()

def data_app(request):
    return render(request, 'ensani/data_page.html')

def activity_logs(request):
    today = timezone.localtime(timezone.now()).date()
    
    # گرفتن مقادیر GET برای فیلترها
    note_type = request.GET.get('note_type', '')
    action = request.GET.get('action', '')
    date_str = request.GET.get('date', today.strftime("%Y-%m-%d"))
    
    logs = ActivityLog.objects.all()
    
    # فیلتر بر اساس تاریخ
    if date_str:
        logs = logs.filter(created_at__date=date_str)
    
    # فیلتر بر اساس نوع یادداشت
    if note_type:
        logs = logs.filter(note_type=note_type)
    
    # فیلتر بر اساس عملیات
    if action:
        logs = logs.filter(action=action)
    
    context = {
        "logs": logs.order_by('-created_at'),
        "note_types": ActivityLog.NoteType.choices,
        "actions": ActivityLog.Action.choices,
        "selected_note_type": note_type,
        "selected_action": action,
        "selected_date": date_str,
    }
    return render(request, 'ensani/activity_logs.html', context)