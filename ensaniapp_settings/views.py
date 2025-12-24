from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import EnsaniSettingsForm,NewPeriodForm
from .models import EnsaniSettings


class CreateOrUpdateSettings(LoginRequiredMixin, View):
    def get(self, request):
        en = EnsaniSettings.objects.filter().all().last()
        form = EnsaniSettingsForm()
        period_form = NewPeriodForm()

        if en is not None:
            form.initial['farmande_razme_moghadamati'] = en.farmande_razme_moghadamati
            form.initial['modire_niroye_ensani'] = en.modire_niroye_ensani
            form.initial['karshenas_manabe_ensani'] = en.karshenas_manabe_ensani
            form.initial['shoare_sall'] = en.shoare_sall
            form.initial['shomare_dore'] = en.shomare_dore
            form.initial['esmedore'] = en.esmedore
            form.initial['tatbigh'] = en.tatbigh
            
            form.initial['saghf_paziresh'] = en.saghf_paziresh
            form.initial['sall'] = en.sall
            form.initial['mahezam'] = en.mahezam
            form.initial['shomare_name_shoro_doreh'] = en.shomare_name_shoro_doreh
            form.initial['saghfi_eblaghi'] = en.saghfi_eblaghi
            # gardeshkar
            form.initial['hokme_darje_gardeshkar'] = en.hokme_darje_gardeshkar
            form.fields['tarikh_hokme_darje_gardeshkar'].widget.attrs['data-initial'] = en.tarikh_hokme_darje_gardeshkar or ''
            
            # signiture
            form.initial['emza_farmande'] = en.emza_farmande
            form.initial['emza_karshenas_manabe_ensani'] = en.emza_karshenas_manabe_ensani
            form.initial['emza_masole_niro_ensani'] = en.emza_masole_niro_ensani

            form.fields['tarihke_name_shoro_doreh'].widget.attrs['data-initial'] = en.tarihke_name_shoro_doreh or ''
            form.fields['tarikhpaziresh'].widget.attrs['data-initial'] = en.tarikhpaziresh or ''
            form.fields['tarikhetmampaziresh'].widget.attrs['data-initial'] = en.tarikhetmampaziresh or ''
            form.fields['tarihkeshorodoreh'].widget.attrs['data-initial'] = en.tarihkeshorodoreh or ''
            form.fields['tarihkepayanedore'].widget.attrs['data-initial'] = en.tarihkepayanedore or ''
            form.fields['tarikhezam'].widget.attrs['data-initial'] = en.tarikhezam or ''

        cx = {'form': form,'en':en,'period_form':period_form}
        return render(request, 'ensaniapp_settings/CreateOrUpdateSettings.html', cx)

    def post(self, request):
        en = EnsaniSettings.objects.filter().all().last()
        form = EnsaniSettingsForm(request.POST or None)
        period_form = NewPeriodForm()
        
        if not form.is_valid():
            form.initial['farmande_razme_moghadamati'] = en.farmande_razme_moghadamati
            form.initial['modire_niroye_ensani'] = en.modire_niroye_ensani
            form.initial['karshenas_manabe_ensani'] = en.karshenas_manabe_ensani
            form.initial['shoare_sall'] = en.shoare_sall
            form.initial['shomare_dore'] = en.shomare_dore
            form.initial['esmedore'] = en.esmedore
            form.initial['tatbigh'] = en.tatbigh
            
            form.initial['saghf_paziresh'] = en.saghf_paziresh
            form.initial['sall'] = en.sall
            form.initial['mahezam'] = en.mahezam
            form.initial['shomare_name_shoro_doreh'] = en.shomare_name_shoro_doreh
            form.initial['saghfi_eblaghi'] = en.saghfi_eblaghi
            # gardeshkar
            form.initial['hokme_darje_gardeshkar'] = en.hokme_darje_gardeshkar
            form.fields['tarikh_hokme_darje_gardeshkar'].widget.attrs['data-initial'] = en.tarikh_hokme_darje_gardeshkar or ''
            # signiture
            form.initial['emza_farmande'] = en.emza_farmande
            form.initial['emza_karshenas_manabe_ensani'] = en.emza_karshenas_manabe_ensani
            form.initial['emza_masole_niro_ensani'] = en.emza_masole_niro_ensani

            form.fields['tarihke_name_shoro_doreh'].widget.attrs['data-initial'] = en.tarihke_name_shoro_doreh or ''
            form.fields['tarikhpaziresh'].widget.attrs['data-initial'] = en.tarikhpaziresh or ''
            form.fields['tarikhetmampaziresh'].widget.attrs['data-initial'] = en.tarikhetmampaziresh or ''
            form.fields['tarihkeshorodoreh'].widget.attrs['data-initial'] = en.tarihkeshorodoreh or ''
            form.fields['tarihkepayanedore'].widget.attrs['data-initial'] = en.tarihkepayanedore or ''
            form.fields['tarikhezam'].widget.attrs['data-initial'] = en.tarikhezam or ''

            cx = {'form': form,'en':en,'period_form':period_form}
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
        sall = form.cleaned_data['sall']
        mahezam = form.cleaned_data['mahezam']
        shomare_name_shoro_doreh = form.cleaned_data['shomare_name_shoro_doreh']
        saghfi_eblaghi = form.cleaned_data['saghfi_eblaghi']
        hokme_darje_gardeshkar = form.cleaned_data['hokme_darje_gardeshkar']

        emza_farmande = form.cleaned_data['emza_farmande']
        emza_karshenas_manabe_ensani = form.cleaned_data['emza_karshenas_manabe_ensani']
        emza_masole_niro_ensani = form.cleaned_data['emza_masole_niro_ensani']
        
        tarikh_hokme_darje_gardeshkar = form.cleaned_data['tarikh_hokme_darje_gardeshkar']
        tarihke_name_shoro_doreh = form.cleaned_data['tarihke_name_shoro_doreh']
        print("form.cleaned_data['tatbigh'] = ",form.cleaned_data['tatbigh'])
        tatbigh  = form.cleaned_data['tatbigh'] 
        if en is None:
            en = EnsaniSettings()
        en.farmande_razme_moghadamati = farmande_razme_moghadamati
        en.modire_niroye_ensani = modire_niroye_ensani
        en.karshenas_manabe_ensani = karshenas_manabe_ensani
        en.shoare_sall = shoare_sall
        en.shomare_dore = shomare_dore
        en.esmedore = esmedore
        en.tatbigh = tatbigh
        
        en.sall = sall
        en.mahezam = mahezam
        en.shomare_name_shoro_doreh = shomare_name_shoro_doreh
        en.saghfi_eblaghi = saghfi_eblaghi
        en.hokme_darje_gardeshkar = hokme_darje_gardeshkar
        
        en.tarikh_hokme_darje_gardeshkar = tarikh_hokme_darje_gardeshkar.replace('/', '-')
        en.tarihke_name_shoro_doreh = tarihke_name_shoro_doreh.replace('/', '-')
        
        en.tarikhpaziresh = tarikhpaziresh.replace('/', '-')
        en.tarikhetmampaziresh = tarikhetmampaziresh.replace('/', '-')
        en.tarihkeshorodoreh = tarihkeshorodoreh.replace('/', '-')
        en.tarihkepayanedore = tarihkepayanedore.replace('/', '-')
        en.saghf_paziresh = saghf_paziresh
        en.tarikhezam = tarikhezam.replace('/', '-')
        en.save()
        return redirect('CreateOrUpdateSettings')



from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import NewPeriodForm
from .backup import backup_sqlite_database_for_new_period
from .cleanup import cleanup_old_period_data
from django.http import HttpResponse
import mimetypes


def new_period_setting(request):
    if request.method == "POST":
        form = NewPeriodForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():

                    # 1️⃣ بکاپ
                    backup_path = backup_sqlite_database_for_new_period()

                    # 2️⃣ ذخیره دوره جدید
                    obj = form.save(commit=True)

                    # 3️⃣ حذف داده‌های قبلی
                    cleanup_old_period_data()

                # 4️⃣ دانلود فایل بکاپ
                with open(backup_path, 'rb') as f:
                    file_data = f.read()

                mime_type, _ = mimetypes.guess_type(str(backup_path))
                mime_type = mime_type or 'application/octet-stream'

                response = HttpResponse(file_data, content_type=mime_type)
                response['Content-Disposition'] = (
                    f'attachment; filename="{backup_path.name}"'
                )

                return response

            except Exception as e:
                messages.error(request, f"خطا: {e}")
                return redirect('CreateOrUpdateSettings')

    return redirect('CreateOrUpdateSettings')
