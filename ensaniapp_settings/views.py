from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
# request, *args, **kwargs
from django.views import View
from .forms import EnsaniSettingsForm
from .models import EnsaniSettings
import jdatetime
import datetime


class CreateOrUpdateSettings(LoginRequiredMixin, View):
    def get(self, request):
        en = EnsaniSettings.objects.filter().all().last()
        form = EnsaniSettingsForm()
        if en is not None:
            form.initial['farmande_razme_moghadamati'] = en.farmande_razme_moghadamati
            form.initial['modire_niroye_ensani'] = en.modire_niroye_ensani
            form.initial['karshenas_manabe_ensani'] = en.karshenas_manabe_ensani
            form.initial['shoare_sall'] = en.shoare_sall
            form.initial['shomare_dore'] = en.shomare_dore
            form.initial['esmedore'] = en.esmedore
            if en.tarikhpaziresh is not None:
                form.initial['tarikhpaziresh'] = en.tarikhpaziresh.togregorian()
            if en.tarikhetmampaziresh is not None:
                form.initial['tarikhetmampaziresh'] = en.tarikhetmampaziresh.togregorian()
            if en.tarihkeshorodoreh is not None:
                form.initial['tarihkeshorodoreh'] = en.tarihkeshorodoreh.togregorian()
            if en.tarihkepayanedore is not None:
                form.initial['tarihkepayanedore'] = en.tarihkepayanedore.togregorian()
            if en.tarikhezam is not None:
                form.initial['tarikhezam'] = en.tarikhezam.togregorian()
            form.initial['saghf_paziresh'] = en.saghf_paziresh
        cx = {'form': form}
        return render(request, 'ensaniapp_settings/CreateOrUpdateSettings.html', cx)

    def post(self, request):
        en = EnsaniSettings.objects.filter().all().last()
        form = EnsaniSettingsForm(request.POST or None)
        if not form.is_valid():
            form.initial['farmande_razme_moghadamati'] = en.farmande_razme_moghadamati
            form.initial['modire_niroye_ensani'] = en.modire_niroye_ensani
            form.initial['karshenas_manabe_ensani'] = en.karshenas_manabe_ensani
            form.initial['shoare_sall'] = en.shoare_sall
            form.initial['shomare_dore'] = en.shomare_dore
            form.initial['esmedore'] = en.esmedore
            if en.tarikhpaziresh is not None:
                form.initial['tarikhpaziresh'] = en.tarikhpaziresh.togregorian()
            if en.tarikhetmampaziresh is not None:
                form.initial['tarikhetmampaziresh'] = en.tarikhetmampaziresh.togregorian()
            if en.tarihkeshorodoreh is not None:
                form.initial['tarihkeshorodoreh'] = en.tarihkeshorodoreh.togregorian()
            if en.tarihkepayanedore is not None:
                form.initial['tarihkepayanedore'] = en.tarihkepayanedore.togregorian()
            if en.tarikhezam is not None:
                form.initial['tarikhezam'] = en.tarikhezam.togregorian()
            cx = {'form': form}
            return render(request, 'ensaniapp_settings/CreateOrUpdateSettings.html', cx)
        farmande_razme_moghadamati = form.cleaned_data['farmande_razme_moghadamati']
        modire_niroye_ensani = form.cleaned_data['modire_niroye_ensani']
        karshenas_manabe_ensani = form.cleaned_data['karshenas_manabe_ensani']
        shoare_sall = form.cleaned_data['shoare_sall']
        shomare_dore = form.cleaned_data['shomare_dore']
        esmedore = form.cleaned_data['esmedore']
        tarikhpaziresh = form.cleaned_data['tarikhpaziresh']
        tarikhetmampaziresh = form.cleaned_data['tarikhetmampaziresh']
        tarihkeshorodoreh = form.cleaned_data['tarihkeshorodoreh']
        tarihkepayanedore = form.cleaned_data['tarihkepayanedore']
        saghf_paziresh = form.cleaned_data['saghf_paziresh']
        tarikhezam = form.cleaned_data['tarikhezam']
        if en is None:
            en = EnsaniSettings()
        en.farmande_razme_moghadamati = farmande_razme_moghadamati
        en.modire_niroye_ensani = modire_niroye_ensani
        en.karshenas_manabe_ensani = karshenas_manabe_ensani
        en.shoare_sall = shoare_sall
        en.shomare_dore = shomare_dore
        en.esmedore = esmedore
        en.tarikhpaziresh = tarikhpaziresh.replace('/', '-')
        en.tarikhetmampaziresh = tarikhetmampaziresh.replace('/', '-')
        en.tarihkeshorodoreh = tarihkeshorodoreh.replace('/', '-')
        en.tarihkepayanedore = tarihkepayanedore.replace('/', '-')
        en.saghf_paziresh = saghf_paziresh
        en.tarikhezam = tarikhezam.replace('/', '-')
        en.save()
        return redirect('CreateOrUpdateSettings')
