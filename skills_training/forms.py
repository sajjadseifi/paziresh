from django import forms
import jdatetime
from .models import HazardSettings

PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر",
    "مرداد", "شهریور", "مهر", "آبان",
    "آذر", "دی", "بهمن", "اسفند"
]

MONTH_CHOICES = [(m, m) for m in PERSIAN_MONTHS]

class HazardSettingsForm(forms.ModelForm):
    # تاریخ‌ها CharField برای دریافت شمسی
    certificate_date = forms.CharField(label='تاریخ صدور گواهی')
    start_date       = forms.CharField(label='تاریخ شروع کلاس')
    end_date         = forms.CharField(label='تاریخ پایان کلاس')
    
    # ماه به صورت Select
    month_name = forms.ChoiceField(label='ماه کلاس',choices=MONTH_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = HazardSettings
        fields = "__all__"
        widgets = {
            "certificate_date": forms.TextInput(attrs={"class": "form-control", "placeholder":"سال/ماه/روز", "dir":"ltr"}),
            "start_date": forms.TextInput(attrs={"class": "form-control", "placeholder":"سال/ماه/روز", "dir":"ltr"}),
            "end_date": forms.TextInput(attrs={"class": "form-control", "placeholder":"سال/ماه/روز", "dir":"ltr"}),
            "letter_number": forms.TextInput(attrs={"class":"form-control","dir":"ltr"}),
            "year": forms.NumberInput(attrs={"class":"form-control","dir":"ltr"}),
            "province": forms.TextInput(attrs={"class":"form-control","dir":"ltr"}),
            "city": forms.TextInput(attrs={"class":"form-control","dir":"ltr"}),
            "first_aid_hours": forms.NumberInput(attrs={"class":"form-control","dir":"ltr"}),
            "hazard_preparedness_hours": forms.NumberInput(attrs={"class":"form-control","dir":"ltr"}),
        }

    # تبدیل تاریخ شمسی به میلادی
    def _clean_shamsi_date(self, value, label):
        if not value:
            return None
        try:
            y, m, d = map(int, value.split("/"))
            return jdatetime.date(y, m, d).togregorian()
        except Exception:
            raise forms.ValidationError(f"فرمت {label} باید سال/ماه/روز باشد")

    def clean_certificate_date(self):
        return self._clean_shamsi_date(self.cleaned_data.get("certificate_date"), "تاریخ گواهی")

    def clean_start_date(self):
        return self._clean_shamsi_date(self.cleaned_data.get("start_date"), "تاریخ شروع دوره")

    def clean_end_date(self):
        return self._clean_shamsi_date(self.cleaned_data.get("end_date"), "تاریخ پایان دوره")

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and end < start:
            self.add_error("end_date", "تاریخ پایان دوره نمی‌تواند قبل از تاریخ شروع باشد")
        return cleaned_data
