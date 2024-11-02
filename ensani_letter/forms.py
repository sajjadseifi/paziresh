from django import forms


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
        widget=forms.Select(
            attrs={'class': "form-control select2"}
        ),
        label='مقصد نامه',
        required=False
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
