from django import forms
from django_jalali import forms as jforms


class EnsaniSettingsForm(forms.Form):
    farmande_razme_moghadamati = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "farmande_razme_moghadamati"}),
        label='فرمانده آموزشگاه رزم مقدماتی',
        required=False
    )
    modire_niroye_ensani = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "modire_niroye_ensani"}),
        label='مدیر نیروی انسانی آموزشگاه رزم مقدماتی',
        required=False
    )
    karshenas_manabe_ensani = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "karshenas_manabe_ensani"}),
        label='کارشناس منابع انسانی سرباز آموزشگاه رزم مقدماتی',
        required=False
    )
    shoare_sall = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "shoare_sall"}),
        label='شعار سال',
        required=False
    )
    shomare_dore = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "shomare_dore"}),
        label='شماره دوره',
        required=False
    )
    esmedore = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control ", 'id': "esmedore"}),
        label='نام دوره',
        required=False
    )
    tarikhpaziresh = forms.CharField(
        label="تاریخ شروع پذیرش",
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control normal-date"}),
    )
    tarikhetmampaziresh = forms.CharField(
        label="تاریخ پایان پذیرش",
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control normal-date"}),
    )
    tarihkeshorodoreh = forms.CharField(
        label="تاریخ شروع دوره",
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control normal-date"}),
    )
    tarihkepayanedore = forms.CharField(
        label="تاریخ پایان دوره",
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control normal-date"}),
    )
    saghf_paziresh = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "saghf_paziresh"}),
        label='سقف پذیرش',
        required=False
    )
    tarikhezam = forms.CharField(
        label="تاریخ اعزام",
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control normal-date"}),
    )
