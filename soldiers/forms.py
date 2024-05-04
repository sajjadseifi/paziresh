from django import forms
from django.core.exceptions import ValidationError

from soldiers.models import Soldier as sarbaz


class FormSoldiers(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام'
    )
    family = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "family"}),
        label='نام خانوادگی'
    )
    fathers_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "fathers_name"}),
        label='نام پدر'
    )
    National_Code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "National_Code", "disabled": ""}),
        label='کد ملی'
    )
    physical_condition = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت جسمانی'
    )
    Type_of_disease = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نوع بیماری'
    )
    health_insurance_card = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "health_insurance_card"}),
        label='دفترچه بیمه'
    )
    Grade = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی'
    )
    Grade_precise = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی دقیق'
    )
    educational_level_of_the_system = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "educational_level_of_the_system"}),
        label='مقطع تحصیلی سامانه'
    )
    Study_group = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Study_group"}),
        label='گروه تحصیلی'
    )
    marital_status = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت تاهل'
    )
    Religion = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مذهب'
    )
    Date_of_birth = place_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_birth"}),
        label='تاریخ تولد'
    )
    place_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='محل تولد'
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='شماره موبایل'
    )
    home_phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "home_phone_number"}),
        label='شماره منزل'
    )
    Date_of_dispatch = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_dispatch"}),
        label='تاریخ اعزام'
    )
    province_name = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نام استان'
    )
    city_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "city_name"}),
        label='نام شهر'
    )
    Address = forms.CharField()
    Place_of_Issue = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Place_of_Issue"}),
        label='ادرس'
    )
    height = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "height"}),
        label='قد'
    )
    Weight = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Weight"}),
        label='وزن'
    )
    Renewal_of_the_previous_period = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Renewal_of_the_previous_period"}),
        label='تجدید دوره قبل'
    )
    Course_renewal_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Course_renewal_date"}),
        label='تاریخ تجدید دوره قبل'
    )
    Amriye = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='امریه دار'
    )
    Amriye_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='سازمان امریه'
    )
    Sufficiency_of_mobilization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='کفایت بسیج'
    )
    Course_renewal_almahdi = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Course_renewal_almahdi"}),
        label='تجدید دوره المهدی کد دوره'
    )
    Course_renewal_almahdi_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Course_renewal_almahdi_date"}),
        label='تاریخ تجدید دوره المهدی'
    )
    Reason_for_renewing_the_course_almahdi = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Reason_for_renewing_the_course_almahdi"}),
        label='علت تجدید دوره المهدی'
    )
    battalion_group = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نام گروهان'
    )


class FormSoldiersCreate(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام'
    )
    family = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "family"}),
        label='نام خانوادگی'
    )
    fathers_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "fathers_name"}),
        label='نام پدر'
    )
    National_Code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "National_Code"}),
        label='کد ملی'
    )
    physical_condition = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت جسمانی'
    )
    Type_of_disease = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2", 'style': "width: 100%;"}
        ),
        label='نوع بیماری'
    )
    health_insurance_card = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "health_insurance_card"}),
        label='دفترچه بیمه'
    )
    Grade = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی'
    )
    Grade_precise = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی دقیق'
    )
    educational_level_of_the_system = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی سامانه'
    )
    Study_group = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Study_group"}),
        label='گروه تحصیلی'
    )
    marital_status = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت تاهل'
    )
    Religion = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مذهب'
    )
    Date_of_birth = place_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_birth"}),
        label='تاریخ تولد'
    )
    place_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='محل تولد'
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='شماره موبایل'
    )
    home_phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "home_phone_number"}),
        label='شماره منزل'
    )
    Date_of_dispatch = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_dispatch"}),
        label='تاریخ اعزام'
    )
    province_name = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2", 'style': "width: 100%;"}
        ),
        label='نام استان'
    )
    city_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "city_name"}),
        label='نام شهر'
    )
    Address = forms.CharField(
        label='ادرس',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"})
    )
    Place_of_Issue = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Place_of_Issue"}),
        label='محل صدور'
    )
    height = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "height"}),
        label='قد'
    )
    Weight = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Weight"}),
        label='وزن'
    )
    Renewal_of_the_previous_period = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='تجدید دوره'
    )
    Course_renewal_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Course_renewal_date"}),
        label='تاریخ تجدید دوره قبل'
    )
    Reason_for_renewing_the_course = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='علت تجدید دوره'
    )
    Renewal_of_the_previous_period_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Renewal_of_the_previous_period_code"}),
        label='کد دوره'
    )
    Amriye = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='امریه دار'
    )
    Amriye_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='سازمان امریه'
    )
    Sufficiency_of_mobilization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='کفایت بسیج'
    )
    attraction_of_the_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='جذبی'
    )
    Sutter = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='ساتر'
    )
    battalion_group = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نام گروهان'
    )

    def clean_National_Code(self):
        s = sarbaz.objects.filter(National_Code=self.cleaned_data['National_Code']).first()
        if s is not None:
            if s.willing_to_learn is False:
                raise ValidationError("این سرباز باید از طریق کد ملی پذیرش شود")
            raise forms.ValidationError("کد ملی تکراری می باشد")
        else:
            return self.cleaned_data['National_Code']


class SarbazCodeMeli(forms.Form):
    code_meli = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'id': 'codemeli',
               'placeholder': 'کدملی وارد کنید'}),
        label='کدملی', )
