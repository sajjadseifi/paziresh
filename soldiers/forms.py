from django import forms
from django.core.exceptions import ValidationError

from soldiers.models import Soldier as sarbaz


class FormSoldiers(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام',
        required=False
    )
    family = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "family"}),
        label='نام خانوادگی',
        required=False
    )
    fathers_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "fathers_name"}),
        label='نام پدر',
        required=False
    )
    National_Code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "National_Code"}),
        label='کد ملی',
        required=False
    )
    physical_condition = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت جسمانی',
        required=False
    )
    Type_of_disease = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2", 'style': "width: 100%;"}
        ),
        label='نوع بیماری',
        required=False
    )
    health_insurance_card = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "health_insurance_card"}),
        label='دفترچه بیمه',
        required=False
    )
    Grade = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی',
        required=False
    )
    Grade_precise = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی دقیق',
        required=False
    )
    educational_level_of_the_system = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی سامانه',
        required=False
    )
    Study_group = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Study_group"}),
        label='گروه تحصیلی',
        required=False
    )
    marital_status = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت تاهل',
        required=False
    )
    Religion = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مذهب',
        required=False
    )
    Date_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_birth"}),
        label='تاریخ تولد',
        required=False
    )
    place_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='محل تولد',
        required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='شماره موبایل',
        required=False
    )
    home_phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "home_phone_number"}),
        label='شماره منزل',
        required=False
    )
    Date_of_dispatch = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_dispatch"}),
        label='تاریخ اعزام',
        required=False
    )
    province_name = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2", 'style': "width: 100%;"}
        ),
        label='نام استان',
        required=False
    )
    city_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "city_name"}),
        label='نام شهر',
        required=False
    )
    Address = forms.CharField(
        label='ادرس',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    Place_of_Issue = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Place_of_Issue"}),
        label='محل صدور',
        required=False
    )
    height = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "height"}),
        label='قد',
        required=False
    )
    Weight = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Weight"}),
        label='وزن',
        required=False
    )
    Renewal_of_the_previous_period = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='تجدید دوره',
        required=False
    )
    Course_renewal_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Course_renewal_date"}),
        label='تاریخ تجدید دوره قبل',
        required=False
    )
    Reason_for_renewing_the_course = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='علت تجدید دوره',
        required=False
    )
    Renewal_of_the_previous_period_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Renewal_of_the_previous_period_code"}),
        label='کد دوره',
        required=False
    )
    Amriye = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='امریه دار',
        required=False
    )
    Amriye_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='سازمان امریه',
        required=False
    )
    Sufficiency_of_mobilization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='کفایت بسیج',
        required=False
    )
    attraction_of_the_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='جذبی',
        required=False
    )
    Sutter = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='ساتر',
        required=False
    )
    battalion_group = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نام گروهان',
    )
    Relative_to_inclusive = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Relative_to_inclusive"}),
        label='نسبت با فراگیر',
        required=False
    )
    Relative_to_inclusive_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Relative_to_inclusive_number"}),
        label='شماره تماس نسبت فراگیر',
        required=False
    )


class FormSoldiersCreate(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام',
        required=False
    )
    family = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "family"}),
        label='نام خانوادگی',
        required=False
    )
    fathers_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "fathers_name"}),
        label='نام پدر',
        required=False
    )
    National_Code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "National_Code"}),
        label='کد ملی',
        required=False
    )
    physical_condition = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت جسمانی',
        required=False
    )
    Type_of_disease = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2", 'style': "width: 100%;"}
        ),
        label='نوع بیماری',
        required=False
    )
    health_insurance_card = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "health_insurance_card"}),
        label='دفترچه بیمه',
        required=False
    )
    Grade = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی',
        required=False
    )
    Grade_precise = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی دقیق',
        required=False
    )
    educational_level_of_the_system = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی سامانه',
        required=False
    )
    Study_group = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Study_group"}),
        label='گروه تحصیلی',
        required=False
    )
    marital_status = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت تاهل',
        required=False
    )
    Religion = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مذهب',
        required=False
    )
    Date_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_birth"}),
        label='تاریخ تولد',
        required=False
    )
    place_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='محل تولد',
        required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='شماره موبایل',
        required=False
    )
    home_phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "home_phone_number"}),
        label='شماره منزل',
        required=False
    )
    Date_of_dispatch = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_dispatch"}),
        label='تاریخ اعزام',
        required=False
    )
    province_name = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2", 'style': "width: 100%;"}
        ),
        label='نام استان',
        required=False
    )
    city_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "city_name"}),
        label='نام شهر',
        required=False
    )
    Address = forms.CharField(
        label='ادرس',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    Place_of_Issue = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Place_of_Issue"}),
        label='محل صدور',
        required=False
    )
    height = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "height"}),
        label='قد',
        required=False
    )
    Weight = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Weight"}),
        label='وزن',
        required=False
    )
    Renewal_of_the_previous_period = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='تجدید دوره',
        required=False
    )
    Course_renewal_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Course_renewal_date"}),
        label='تاریخ تجدید دوره قبل',
        required=False
    )
    Reason_for_renewing_the_course = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='علت تجدید دوره',
        required=False
    )
    Renewal_of_the_previous_period_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Renewal_of_the_previous_period_code"}),
        label='کد دوره',
        required=False
    )
    Amriye = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='امریه دار',
        required=False
    )
    Amriye_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='سازمان امریه',
        required=False
    )
    Sufficiency_of_mobilization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='کفایت بسیج',
        required=False
    )
    attraction_of_the_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='جذبی',
        required=False
    )
    Sutter = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='ساتر',
        required=False
    )
    battalion_group = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نام گروهان',
    )
    Relative_to_inclusive = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Relative_to_inclusive"}),
        label='نسبت با فراگیر',
        required=False
    )
    Relative_to_inclusive_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Relative_to_inclusive_number"}),
        label='شماره تماس نسبت فراگیر',
        required=False
    )

    def clean_National_Code(self):
        s = sarbaz.objects.filter(National_Code=self.cleaned_data['National_Code']).first()
        if s is not None:
            if s.willing_to_learn is False:
                raise ValidationError("این سرباز باید از طریق کد ملی پذیرش شود")
            raise forms.ValidationError("کد ملی تکراری می باشد")
        else:
            return self.cleaned_data['National_Code']


class FormSoldiersUpdate(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "name"}),
        label='نام',
        required=False
    )
    family = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "family"}),
        label='نام خانوادگی',
        required=False
    )
    fathers_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "fathers_name"}),
        label='نام پدر',
        required=False
    )
    National_Code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "National_Code"}),
        label='کد ملی',
        required=False
    )
    physical_condition = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت جسمانی',
        required=False
    )
    Type_of_disease = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2", 'style': "width: 100%;"}
        ),
        label='نوع بیماری',
        required=False
    )
    health_insurance_card = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "health_insurance_card"}),
        label='دفترچه بیمه',
        required=False
    )
    Grade = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی',
        required=False
    )
    Grade_precise = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی دقیق',
        required=False
    )
    educational_level_of_the_system = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مقطع تحصیلی سامانه',
        required=False
    )
    Study_group = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Study_group"}),
        label='گروه تحصیلی',
        required=False
    )
    marital_status = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='وضعیت تاهل',
        required=False
    )
    Religion = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='مذهب',
        required=False
    )
    Date_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_birth"}),
        label='تاریخ تولد',
        required=False
    )
    place_of_birth = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='محل تولد',
        required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "place_of_birth"}),
        label='شماره موبایل',
        required=False
    )
    home_phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "home_phone_number"}),
        label='شماره منزل',
        required=False
    )
    Date_of_dispatch = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Date_of_dispatch"}),
        label='تاریخ اعزام',
        required=False
    )
    province_name = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control select2", 'style': "width: 100%;"}
        ),
        label='نام استان',
        required=False
    )
    city_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "city_name"}),
        label='نام شهر',
        required=False
    )
    Address = forms.CharField(
        label='ادرس',
        widget=forms.Textarea(attrs={'class': "form-control", "rows": "5"}),
        required=False
    )
    Place_of_Issue = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Place_of_Issue"}),
        label='محل صدور',
        required=False
    )
    height = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "height"}),
        label='قد',
        required=False
    )
    Weight = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Weight"}),
        label='وزن',
        required=False
    )
    Renewal_of_the_previous_period = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='تجدید دوره',
        required=False
    )
    Course_renewal_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Course_renewal_date"}),
        label='تاریخ تجدید دوره قبل',
        required=False
    )
    Reason_for_renewing_the_course = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='علت تجدید دوره',
        required=False
    )
    Renewal_of_the_previous_period_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Renewal_of_the_previous_period_code"}),
        label='کد دوره',
        required=False
    )
    Amriye = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='امریه دار',
        required=False
    )
    Amriye_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='سازمان امریه',
        required=False
    )
    Sufficiency_of_mobilization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='کفایت بسیج',
        required=False
    )
    attraction_of_the_organization = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='جذبی',
        required=False
    )
    Sutter = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='ساتر',
        required=False
    )
    battalion_group = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نام گروهان',
    )
    Relative_to_inclusive = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Relative_to_inclusive"}),
        label='نسبت با فراگیر',
        required=False
    )
    Relative_to_inclusive_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "Relative_to_inclusive_number"}),
        label='شماره تماس نسبت فراگیر',
        required=False
    )


class SarbazCodeMeli(forms.Form):
    code_meli = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'id': 'codemeli',
               'placeholder': 'کدملی وارد کنید'}),
        label='کدملی', )

    def clean_code_meli(self):
        s = sarbaz.objects.filter(National_Code=self.cleaned_data['code_meli']).first()
        if s is None:
            raise ValidationError("این سرباز با این کد ملی وجود ندارد")
        if s.willing_to_learn is True:
            raise ValidationError("این سرباز پذیرش شده")
        return self.cleaned_data['code_meli']


class FormAddExelToDb(forms.Form):
    file = forms.FileField()


class FormSaterGroup(forms.Form):
    start = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "start"}),
        label='از',
        required=False
    )
    end = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "end"}),
        label='تا',
        required=False
    )
    type = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label='نوع ساتر',
        required=False
    )


class FormMoarefiGroup(forms.Form):
    start = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "start"}),
        label='از',
        required=False
    )
    end = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "end"}),
        label='تا',
        required=False
    )


class FormUpdatePazireshHazer(forms.Form):
    file = forms.FileField()


class FormUpdatePazireshshode(forms.Form):
    file = forms.FileField()
