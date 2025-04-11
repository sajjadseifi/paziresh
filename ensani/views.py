from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from soldiers.models import Soldier
from battalions.models import battalion, battalion_group
from ensaniapp_settings.models import EnsaniSettings
from django.contrib.auth.decorators import login_required

class panel_home(LoginRequiredMixin, View):
    def get(self, request):
        soldire = Soldier.objects.filter().all()
        amar_kol = soldire.count()
        amar_kole_hezer_bekhdmat = soldire.filter(willing_to_learn=True).all().count()
        amar_kole_paziresh_shode = Soldier.objects.filter(has_been_accepted=True).all().count()
        tatbikh_nashode = Soldier.objects.filter(has_been_accepted=True, in_coures=True, the_medical_commission=False,
                                                 Previous_service_record=False, Sufficiency_of_mobilization=False,
                                                 tatbigh=False, IsCheckout=False).all().count()
        total_tegan_khdmati_in_course = Soldier.objects.filter(has_been_accepted=True, willing_to_learn=True,
                                                               in_coures=True, IsCheckout=False,IsUnit=False).all().count()
        en = EnsaniSettings.objects.filter().first()
        b_soldire = Soldier.objects.filter(has_been_accepted=True, in_coures=True, willing_to_learn=True).all()
        if en.tatbigh is False:
            list_btn = []
            name_list = []
            total_list = []
            gordan = battalion.objects.filter().all().order_by('name')
            for iteam in gordan:
                gorhan = battalion_group.objects.filter(gordan=iteam).order_by('name')
                tt = b_soldire.filter(Gordan=iteam).all().count()
                if tt != 0:
                    total_list.append(tt)
                    name_list.append(iteam.name)
                for iteam in gorhan:
                    t = b_soldire.filter(battalion_group=iteam).all().count()
                    if t != 0:
                        list_btn.append({'gordan': iteam.gordan.name, 'gorohan': iteam.name, 'count': t})
        else:

            list_btn = []
            name_list = []
            total_list = []
            gordan = battalion.objects.filter().all().order_by('name')
            for iteam in gordan:
                gorhan = battalion_group.objects.filter(gordan=iteam).order_by('name')
                tt = b_soldire.filter(t_Gordan=iteam).all().count()
                if tt != 0:
                    total_list.append(tt)
                    name_list.append(iteam.name)
                for iteam in gorhan:
                    t = b_soldire.filter(t_battalion_group=iteam).all().count()
                    if t != 0:
                        list_btn.append({'gordan': iteam.gordan.name, 'gorohan': iteam.name, 'count': t})

        cx = {'amar_kol': amar_kol, 'amar_kole_hezer_bekhdmat': amar_kole_hezer_bekhdmat,
              'amar_kole_paziresh_shode': amar_kole_paziresh_shode, 'tatbikh_nashode': tatbikh_nashode,
              'total_tegan_khdmati_in_course': total_tegan_khdmati_in_course, 'list_btn': list_btn,
              'name_list': name_list, 'total_list': total_list}
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
