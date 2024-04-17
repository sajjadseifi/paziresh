from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import resolve_url
from django.urls import reverse
from django.views import View
from soldiers.models import Soldier as sarbaz
from .forms import SarbazCodeMeli


def paziresh_code_meli(request, *args, **kwargs):
    sarbaz_code_meli = SarbazCodeMeli(request.POST or None)
    if sarbaz_code_meli.is_valid():
        code_meli = sarbaz_code_meli.cleaned_data.get('code_meli')
        print(code_meli)
        return HttpResponseRedirect(reverse("get_sarbaz", args=[code_meli]))

    return render(request, 'soldiers/paziresh_idcode_view.html', context={'SarbazCodeMeli': sarbaz_code_meli})


class sabte_paziresh(LoginRequiredMixin, View):
    template = 'soldiers/sabte_paziresh_view.html'

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(National_Code=pk).first()
        cx = {'sarbaz': my_sarbaz}
        return render(request, self.template, cx)

    def post(self, request):
        cx = {}
        return render(request, self.template, cx)


class moarefi_be_gordan(LoginRequiredMixin, View):
    template = 'soldiers/moarefi_be_gordan.html'

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(National_Code=pk).first()
        cx = {'sarbaz': my_sarbaz}
        return render(request, self.template, cx)

    def post(self, request):
        cx = {}
        return render(request, self.template, cx)


class sater(LoginRequiredMixin, View):

    def get(self, request, pk):
        my_sarbaz = sarbaz.objects.filter(National_Code=pk).first()
        cx = {'sarbaz': my_sarbaz}
        return render(request, 'soldiers/sater_adi_page.html', cx)
