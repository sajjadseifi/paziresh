from django import forms
from .models import RawLetter,LetterType
from datetime import datetime

class CreateCheckoutLetterFrom(forms.Form):
    soldire = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='سرباز',
        required=False
    )
    description = forms.CharField(
        label='توضیحات',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    c_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='علت تسویه حساب',
        required=False
    )


class CreateRegisterLetterFrom(forms.Form):
    soldire = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='سرباز',
        required=False
    )
    description = forms.CharField(
        label='توضیحات',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    destination = forms.CharField(
        label='مقصد نامه',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    destination_letter_number = forms.CharField(
        label='شماره نامه وارده',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    destination_letter_date = forms.CharField(
        label='تاریخ نامه وارده',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )

    in_come_submit_locations = forms.CharField(
        label='مبداء صادر کننده',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )


class CreateMoarefiFrom(forms.Form):
    soldire = forms.ChoiceField(
        widget=forms.Select(attrs={'class': "form-control select2"}),
        label='سرباز',
        required=True
    )
    destination = forms.CharField(
        label='مقصد نامه',
        widget=forms.TextInput(attrs={'class': "form-control"}),
        required=True,
    )

    tarihki_moarefi = forms.CharField(
        label='تاریخ معرفی',
        widget=forms.TextInput(attrs={'class': "form-control"}),
        required=True,
    )
    no_moarefi = forms.CharField(
        label='علت معرفی',
        widget=forms.TextInput(attrs={'class': "form-control"}),
        required=True,
    )

    suttr = forms.ChoiceField(
        choices=[("گرفته است", "گرفته است"), ("نگرفته است", "نگرفته است")],
        widget=forms.Select(attrs={'class': "form-control select2"}),
        label='ساتر'
    )


class CreateCommissionLetterFrom(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "subject"}),
        label='موضوع نامه',
        required=False
    )
    description = forms.CharField(
        label='توضیحات',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    destination = forms.ChoiceField(
        label='مقصد نامه',
        required=True,
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
    )


class CreateBeforeCourseCommissionLetterFrom(forms.Form):
    description = forms.CharField(
        label='توضیحات',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    soldire = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='سرباز',
        required=False
    )


class CreateTrainingInquiryLetterFrom(forms.Form):
    soldire = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='سرباز',
        required=False
    )


class CreateRunAwayLetterFrom(forms.Form):
    soldire = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='سرباز',
        required=False
    )
    type = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='دلیل فرار',
        required=False
    )
    date = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "date"}),
        label='تاریخ فرار',
        required=False
    )


class CreateFarajaLetterFrom(forms.Form):
    soldire = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='سرباز',
        required=False
    )
    elat = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "elat"}),
        label='علت معرفی',
        required=False
    )
    faraja_leter_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "elat"}),
        label='شماره نامه فراجا',
        required=False
    )
    faraja_leter_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "elat"}),
        label='تاریخ نامه فراجا',
        required=False
    )



class CreateRawLetterForm(forms.Form):
    # =========================
    # فیلدهای سرباز
    # =========================
    soldier_national_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "id_soldier_national_code"}),
        label='کد ملی',
        required=False
    )

    soldier_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "id_soldier_name"}),
        label='نام',
        required=False
    )

    soldier_family = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "id_soldier_family"}),
        label='نام خانوادگی',
        required=False
    )

    soldier_fathers_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "id_soldier_fathers_name"}),
        label='نام پدر',
        required=False
    )

    soldier_acceptance_code = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': "form-control", "id": "id_soldier_acceptance_code"}),
        label='کد پذیرش',
        required=False
    )

    soldier_date_of_dispatch = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "id_soldier_date_of_dispatch"}),
        label='تاریخ اعزام',
        required=False
    )

    # =========================
    # فیلدهای نامه
    # =========================
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "id_title"}),
        label='عنوان نامه',
        required=False
    )

    letter_type = forms.ChoiceField(
        choices=[("", "یک نوع نامه انتخاب یا وارد کنید")] + list(LetterType.choices),
        widget=forms.Select(attrs={'class': "form-control select2", "id": "id_letter_type"}),
        label='نوع نامه',
        required=False,
    )

    return_to_number  = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "return_to_number"}),
        label='بازگشت به شماره نامه (اختیاری)',
        required=False
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': "form-control", "type": "date", "id": "id_date"}),
        label='تاریخ نامه',
        required=False
    )

    destination = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "id_destination"}),
        label='گیرنده/مقصد',
        required=False
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': "form-control", "rows": 4, "id": "id_description"}),
        label='توضیحات',
        required=True
    )

    status = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", "id": "id_status"}),
        label='وضعیت',
        required=False
    )

    # =========================
    # مقداردهی اولیه
    # =========================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('date'):
            self.fields['date'].initial = datetime.now().strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        # اگر عنوان انتخاب شده در choices موجود باشد، letter_type همان مقدار است
        found = False
        for choice_value, choice_label in LetterType.choices:
            if title == choice_label:
                cleaned_data['letter_type'] = choice_value
                found = True
                break

        # اگر عنوان در choices نبود، letter_type = other
        if not found:
            cleaned_data['letter_type'] = 'other'

        return cleaned_data