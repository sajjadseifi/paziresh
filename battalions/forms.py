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


class BattalionGroupForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام گروهان'
    )
    gordan = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='گردان'
    )
    ebtedai = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "ebtedai", 'id': "ebtedai"}
        ),
        label='ابتدایی',
        required=False
    )
    rahnamai = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "rahnamai", 'id': "rahnamai"}
        ),
        label='راهنمایی',
        required=False
    )
    dabirestan = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "dabirestan", 'id': "dabirestan"}
        ),
        label='دبیرستان',
        required=False
    )
    zirediplom = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "zirediplom", 'id': "zirediplom"}
        ),
        label='زیر دیپلم',
        required=False
    )
    diplom = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "diplom", 'id': "diplom"}
        ),
        label='دیپلم',
        required=False
    )
    ofghdiplom = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "ofghdiplom", 'id': "ofghdiplom"}
        ),
        label='فوق دیپلم',
        required=False
    )
    lisans = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "lisans", 'id': "lisans"}
        ),
        label='لیسانس',
        required=False
    )
    ofghlisans = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "ofghlisans", 'id': "ofghlisans"}
        ),
        label='فوق لیسانس',
        required=False
    )
    doctra = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "doctra", 'id': "doctra"}
        ),
        label='دکترا',
        required=False
    )
    shie = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "shie", 'id': "shie"}
        ),
        label='شیعه',
        required=False
    )
    ahle_tasnon = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "ahle_tasnon", 'id': "ahle_tasnon"}
        ),
        label='اهل تسنن',
        required=False
    )
    zarfiat = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "zarfiat"}),
        label='ظرفیت گروهان'
    )
    takmilzarmit = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'type': "checkbox", 'name': "takmilzarmit", 'id': "takmilzarmit"}
        ),
        label='تکمیل بودن ظرفیت',
        required=False
    )
    order = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "order"}),
        label='اولویت مرتب سازی'
    )
