from django import forms


class BattalionForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام گردان'
    )

    order = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "order"}),
        label='اولویت مرتب سازی'
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "IsActive", 'id': "IsActive"}
        ),
        label='فعال/غیرفعال',
        required=False
    )
