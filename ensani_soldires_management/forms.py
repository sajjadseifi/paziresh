from django import forms


class FormUpdateGordan(forms.Form):
    file = forms.FileField()


class Formjazbi(forms.Form):
    file = forms.FileField()
    type = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نوع جذب',
        required=False
    )


class FormYegankhedmati(forms.Form):
    file = forms.FileField()
    type = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نوع سرباز',
        required=False
    )


class FormUpdateAllSoldiresHasbenAceptedInCourse(forms.Form):
    file = forms.FileField()


class FormUpdateAllSoldires(forms.Form):
    file = forms.FileField()
