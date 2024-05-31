from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from soldiers.models import Soldier


class panel_home(LoginRequiredMixin, View):
    def get(self, request):
        soldire = Soldier.objects.filter().all()
        amar_kol = soldire.count()
        amar_kole_hezer_bekhdmat = soldire.filter(willing_to_learn=True).all().count()

        cx = {'amar_kol': amar_kol, 'amar_kole_hezer_bekhdmat': amar_kole_hezer_bekhdmat}
        return render(request, 'ensani/panel_home_page.html', cx)


def support(request, *args, **kwargs):
    return render(request, 'ensani/poshtibani.html')


# Create your views here.
def header_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Header.html')


def header_references_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_HeaderReferences.html')


def navbar_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Navbar.html')


def footer_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Footer.html')


def footer_references_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_FooterReferences.html')
