from django import forms

class EditUnitForm(forms.Form):
    unit_name_orginal = forms.CharField(
      label="نام اولیه یگان",
      required=True,
      widget=forms.TextInput(attrs={
         "id": "unit_name_original",
         "name": "unit_name_original",
         "type": "hidden"
      })
    )
    unit_type_orginal = forms.CharField(
      label="نوع اولیه یگان",
      required=True,
      widget=forms.TextInput(attrs={
         "id": "unit_type_orginal",
         "name": "unit_type_orginal",
         "type": "hidden"
      })
    )
    unit_name = forms.CharField(
      label="نام یگان",
      required=False,
      widget=forms.TextInput(attrs={
         "class": "form-control select2-allow-new",
         "id": "unit_name"
      })
    )

    unit_type = forms.ChoiceField(
        label="نوع یگان",
        required=False,
        widget=forms.Select(attrs={
            "class": "form-control select2-no-new",
            "id": "unit_type"
        })
    )
    apply_to_soldiers = forms.BooleanField(
        label="اعمال وضعیت تطبیق روی سربازان",
        required=False,
        widget=forms.CheckboxInput(attrs={"id": "apply_to_soldiers"})
    )
    unit_match = forms.ChoiceField(
        label="وضعیت یگان",
        required=False,
        choices=[("match", "تطبیق"), ("no_match", "عدم تطبیق")],
        widget=forms.RadioSelect(attrs={
            "class": "btn-group",
            "id": "unit_status"
        })
    )
    def __init__(self, *args, **kwargs):
        unit_names = kwargs.pop("unit_names", [])
        unit_types = kwargs.pop("unit_types", [])
        super().__init__(*args, **kwargs)
        self.fields["unit_name"].choices = [(n, n) for n in unit_names if n]
        self.fields["unit_type"].choices = [(t, t) for t in unit_types if t]
         
         # unit_type اختیاری: اضافه کردن گزینه خالی
        self.fields["unit_type"].choices = [("", "انتخاب کنید")] + [(t, t) for t in unit_types if t]
        
        
    def clean(self):
      cleaned_data = super().clean()
      for field in ["unit_name", "unit_name_orginal", "unit_type", "unit_type_orginal"]:
         if cleaned_data.get(field) in ["None", ""]:
               cleaned_data[field] = None
      return cleaned_data