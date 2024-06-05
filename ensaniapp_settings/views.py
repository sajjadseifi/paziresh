from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
# request, *args, **kwargs
from django.views import View
from .forms import EnsaniSettingsForm
from .models import EnsaniSettings


class CreateOrUpdateSettings(LoginRequiredMixin, View):
    def get(self, request):
        en = EnsaniSettings.objects.filter().all().last()
        form = EnsaniSettingsForm()
        if en is None:
            en = EnsaniSettings()
        else:
            form.initial['farmande_razme_moghadamati'] = en.farmande_razme_moghadamati
            form.initial['modire_niroye_ensani'] = en.modire_niroye_ensani
            form.initial['karshenas_manabe_ensani'] = en.karshenas_manabe_ensani
            form.initial['shoare_sall'] = en.shoare_sall
            form.initial['shomare_dore'] = en.shomare_dore
            form.initial['esmedore'] = en.esmedore
            form.initial['tarikhpaziresh'] = en.tarikhpaziresh
            form.initial['tarikhetmampaziresh'] = en.tarikhetmampaziresh
            form.initial['tarihkeshorodoreh'] = en.tarihkeshorodoreh
            form.initial['tarihkepayanedore'] = en.tarihkepayanedore
            form.initial['tarikhezam'] = en.tarikhezam
            form.initial['saghf_paziresh'] = en.saghf_paziresh

        cx = {'form': form}
        return render(request, 'ensaniapp_settings/CreateOrUpdateSettings.html', cx)
