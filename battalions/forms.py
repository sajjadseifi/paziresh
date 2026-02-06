from django import forms


class BattalionForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام گردان'
    )
    commander = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='فرمانده گردان',
        required=False,
    )
    gcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='کد گردانی'
    )

    order = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "order"}),
        label='اولویت مرتب سازی'
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "IsActive", 'id': "IsActive"}),
        label='فعال/غیرفعال',
        required=False
    )


class BattalionGroupForm(forms.Form):
    status_types = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(attrs={'class':'checkbox-multiple md3'}),
        required=False,
        label='وضعیت برگه سبز',
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام گروهان'
    )
    commander = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='فرمانده گروهان',
        required=False,
    )
    
    gordan = forms.ChoiceField(
        widget=forms.Select(attrs={'class': "form-control"}),
        label='گردان'
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "is_active", 'id': "is_active"}),
        label='فعال/غیرفعال',
        required=False
    )
    zirediplom = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "zirediplom", 'id': "zirediplom"}),
        label='زیر دیپلم',
        required=False
    )
    diplom = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "diplom", 'id': "diplom"}),
        label='دیپلم',
        required=False
    )
    ofghdiplom = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "ofghdiplom", 'id': "ofghdiplom"}),
        label='فوق دیپلم',
        required=False
    )
    lisans = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "lisans", 'id': "lisans"}),
        label='لیسانس',
        required=False
    )
    ofghlisans = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "ofghlisans", 'id': "ofghlisans"}),
        label='فوق لیسانس',
        required=False
    )
    doctra = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "doctra", 'id': "doctra"}),
        label='دکترا',
        required=False
    )
    shie = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "shie", 'id': "shie"}),
        label='شیعه',
        required=False
    )
    ahle_tasnon = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "ahle_tasnon", 'id': "ahle_tasnon"}),
        label='اهل تسنن',
        required=False
    )
    zarfiat = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control text-left",'dir':'ltr', 'id': "zarfiat"}),
        label='ظرفیت گروهان',
        initial=0,
    )
    takmilzarmit = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "takmilzarmit", 'id': "takmilzarmit"}),
        label='تکمیل بودن ظرفیت',
        required=False
    )
    order = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control text-left",'dir':'ltr', 'id': "order"}),
        label='اولویت مرتب سازی',
        initial=0,
    )
    salemm = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "takmilzarmit", 'id': "takmilzarmit"}),
        label='سالم',
        required=False
    )
    moafazrazm = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "takmilzarmit", 'id': "takmilzarmit"}),
        label='معاف ازرزم',
        required=False
    )
    gorehbe = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "takmilzarmit", 'id': "takmilzarmit"}),
        label='گروه ب',
        required=False
    )
    moafazrazm_gorehbe = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "takmilzarmit", 'id': "takmilzarmit"}),
        label='معاف از رزم + گروه ب',
        required=False
    )
    gharagah_sazandegi_khatam = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'type': "checkbox", 'name': "gharagah_sazandegi_khatam", 'id': "gharagah_sazandegi_khatam"}),
        label='قرارگاه سازندگی خاتم',
        required=False
    )
