from django import forms
import jdatetime
from .models import HazardSettings

class HazardSettingsForm(forms.ModelForm):
    class Meta:
        model = HazardSettings
        fields = "__all__"
        widgets = {
            "certificate_date": forms.TextInput(attrs={
                "class": "form-control", "dir":"ltr", "placeholder":"سال/ماه/روز"
            }),
            "start_date": forms.TextInput(attrs={
                "class": "form-control", "dir":"ltr", "placeholder":"سال/ماه/روز"
            }),
            "end_date": forms.TextInput(attrs={
                "class": "form-control", "dir":"ltr", "placeholder":"سال/ماه/روز"
            }),
            "letter_number": forms.TextInput(attrs={"class": "form-control","dir":"ltr"}),
            "year": forms.NumberInput(attrs={"class": "form-control","dir":"ltr"}),
            "month_name": forms.TextInput(attrs={"class": "form-control","dir":"ltr"}),
            "first_aid_hours": forms.NumberInput(attrs={"class": "form-control","dir":"ltr"}),
            "hazard_preparedness_hours": forms.NumberInput(attrs={"class": "form-control","dir":"ltr"}),
        }

    def _clean_shamsi_date(self, value, field_name):
        if isinstance(value, str):
            try:
                y, m, d = map(int, value.split("/"))
                return jdatetime.date(y, m, d).togregorian()
            except:
                raise forms.ValidationError(f"فرمت {field_name} باید سال/ماه/روز باشد")
        return value

    def clean_certificate_date(self):
        return self._clean_shamsi_date(self.cleaned_data.get("certificate_date"), "تاریخ گواهی")

    def clean_start_date(self):
        return self._clean_shamsi_date(self.cleaned_data.get("start_date"), "تاریخ شروع دوره")

    def clean_end_date(self):
        return self._clean_shamsi_date(self.cleaned_data.get("end_date"), "تاریخ پایان دوره")
