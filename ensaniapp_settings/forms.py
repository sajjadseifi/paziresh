from django import forms
from django_jalali import forms as jforms
from .models import EnsaniSettings
from .widgets import CustomImageInput

class EnsaniSettingsForm(forms.Form):
    class Meta:
        model = EnsaniSettings
        fields = "__all__"
        
    farmande_razme_moghadamati = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "farmande_razme_moghadamati"}),
        label='فرمانده آموزشگاه',
        required=False
    )
    modire_niroye_ensani = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "modire_niroye_ensani"}),
        label='مدیر نیروی انسانی',
        required=False
    )
    karshenas_manabe_ensani = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "karshenas_manabe_ensani"}),
        label='کارشناس منابع سرباز',
        required=False
    )
    shoare_sall = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "shoare_sall"}),
        label='شعار سال',
        required=False
    )
    tatbigh = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': "form-control hidden", 'id': "tatbigh"}),
        label='تطبیق سامانه',
        required=False,
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
    shomare_name_shoro_doreh = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
        label='شماره نامه ابلاغ دوره',
        required=False
    )

    tarihke_name_shoro_doreh = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control normal-date"}),
        label='تاریخ نامه ابلاغ دوره',
        required=False
    )

    mahezam = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
        label='ماه اعزام',
        required=False
    )

    sall = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
        label='سال',
        required=False
    )

    saghfi_eblaghi = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
        label='سقف نامه',
        required=False
    )

    hokme_darje_gardeshkar = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
        label='حکم درجه گردشکار',
        required=False
    )

    tarikh_hokme_darje_gardeshkar = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control normal-date"}),
        label='تاریخ حکم درجه گردشکار',
        required=False
    )
    emza_karshenas_manabe_ensani = forms.ImageField(
        label='امضای کارشناس منابع سرباز',
        required=False,
        widget=CustomImageInput()
    )

    emza_masole_niro_ensani = forms.ImageField(
        label='امضای مسئول نیروی انسانی',
        required=False,
        widget=CustomImageInput()
    )

    emza_farmande = forms.ImageField(
        label='امضای فرمانده آموزشگاه',
        required=False,
        widget=CustomImageInput()
    )
    
import re
import datetime
import jdatetime
from django import forms
from .models import EnsaniSettings

class NewPeriodForm(forms.Form):

    shomare_dore = forms.CharField(
        label='شماره دوره',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: 1404-01'
        })
    )

    name_dore = forms.CharField(
        label='نام دوره',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'مثال : میثم گل بابازاده' })
    )

    tarikhezam = forms.CharField(
        label="تاریخ اعزام",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control normal-date'})
    )

    tarikh_shoro = forms.CharField(
        label='تاریخ شروع دوره',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control normal-date '})
    )

    modat_rooz_paziresh = forms.IntegerField(
        label='مدت روز پذیرش',
        required=True,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    modat_rooz_amozesh = forms.IntegerField(
        label='مدت روز آموزش',
        required=True,
        initial=54,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    rule_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'id': 'rule_accepted'}),
        label='با شرایط و قوانین موافقم',
        required=True,
        initial=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # شماره دوره خودکار
        last_setting = EnsaniSettings.objects.last()
        if last_setting and last_setting.shomare_dore:
            self.fields['shomare_dore'].initial = self._increase_period_number(last_setting.shomare_dore)

        # تاریخ امروز شمسی
        today = jdatetime.date.today()
        # نیمه ماه
        if today.day <= 15:
            start_date = jdatetime.date(today.year, today.month, 1)  # نیمه اول ماه → روز 01 همان ماه
        else:
            # نیمه دوم ماه → روز 01 ماه بعد
            if today.month < 12:
                start_date = jdatetime.date(today.year, today.month + 1, 1)
            else:
                start_date = jdatetime.date(today.year + 1, 1, 1)

        self.fields['tarikhezam'].widget.attrs['data-initial'] = start_date
        self.fields['tarikh_shoro'].widget.attrs['data-initial'] = start_date

    def _increase_period_number(self, value: str) -> str:
        """
        اگر انتهای مقدار عدد باشد → +1
        اگر عدد نداشت → '1' به انتها اضافه می‌کند
        """
        match = re.search(r'(.*?)(\d+)$', value)
        if match:
            prefix, number = match.groups()
            return f"{prefix}{int(number) + 1}"
        return f"{value}1"

    def _parse_jdate(self, value: str):
        """
        تبدیل '1404-10-01' یا '1404/10/01' به jdatetime.date
        """
        if not value:
            return None

        value = value.replace('-', '/')
        y, m, d = map(int, value.split('/'))
        return jdatetime.date(y, m, d)

    def save(self, commit=True):
        cd = self.cleaned_data

        obj = EnsaniSettings.objects.all().first()

        # -------- DORE --------
        obj.shomare_dore = cd.get('shomare_dore')
        obj.esmedore = cd.get('name_dore')

        obj.tarikhezam = self._parse_jdate(cd.get('tarikhezam'))
        obj.tarihkeshorodoreh = self._parse_jdate(cd.get('tarikh_shoro'))
        obj.hokme_darje_gardeshkar = ''
        obj.tarikh_hokme_darje_gardeshkar = None
        # سال و ماه اعزام (از تاریخ اعزام)
        if obj.tarikhezam:
            obj.sall = str(obj.tarikhezam.year)
            obj.mahezam = obj.tarikhezam.strftime('%B')
        # -------- PAZIRESH (مثال محاسباتی) --------
        if obj.tarihkeshorodoreh:
            # پایان پذیرش = روز شروع دوره
            obj.tarikhpaziresh = obj.tarihkeshorodoreh
            # تاریخ شروع پذیرش = 5 روز قبل
            mrp = cd.get('modat_rooz_paziresh', 0)
            if mrp > 1:
                mrp -= 1 
            obj.tarikhetmampaziresh = obj.tarihkeshorodoreh + jdatetime.timedelta(days=mrp)
            # پایان دوره = شروع + مدت آموزش
            mra = cd.get('modat_rooz_amozesh', 0)
            if mra > 1:
                mra -= 1
            obj.tarihkepayanedore = obj.tarihkeshorodoreh + jdatetime.timedelta(days=mra)

        if commit:
            obj.save()

        return obj

