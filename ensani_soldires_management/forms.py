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


class FormRankGroup(forms.Form):
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


class FormAmirMahart(forms.Form):
    excel_file = forms.FileField()


from django import forms
from .access import get_user_soldiers


class TopSoldiersForm(forms.Form):
    soldier_1 = forms.ChoiceField(label='نفر اول', required=False)
    soldier_2 = forms.ChoiceField(label='نفر دوم', required=False)
    soldier_3 = forms.ChoiceField(label='نفر سوم', required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # دریافت سربازان مجاز
        soldiers = get_user_soldiers(user).filter(in_coures=True, willing_to_learn=True)
        choices = [('', 'انتخاب کنید')] + [(s.id, f"{s.name} {s.family} - {s.National_Code}") for s in soldiers]

        self.fields['soldier_1'].choices = choices
        self.fields['soldier_2'].choices = choices
        self.fields['soldier_3'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        selected = [
            cleaned_data.get('soldier_1'),
            cleaned_data.get('soldier_2'),
            cleaned_data.get('soldier_3')
        ]
        # حذف مقادیر خالی
        selected_ids = [s for s in selected if s]

        # جلوگیری از انتخاب تکراری
        if len(selected_ids) != len(set(selected_ids)):
            raise forms.ValidationError("یک سرباز نمی‌تواند در دو رتبه انتخاب شود.")

        return cleaned_data
    
from django.forms import formset_factory

PROBLEM_FIELDS = [
    'father_veteran', 'child_under_coverage', 'father_under_coverage', 'mother_under_coverage',
    'brother_under_coverage', 'sister_under_coverage', 'only_child', 'only_son', 'divorced_child',
    'family_support', 'father_sick', 'mother_sick', 'father_disabled', 'father_deceased',
    'mother_deceased', 'need_declared', 'married', 'has_child','description'
]

PROBLEM_LABELS = {
    'father_veteran': 'پدر ایثارگر',
    'child_under_coverage': 'فرد تحت پوشش',
    'father_under_coverage': 'پدر تحت پوشش',
    'mother_under_coverage': 'مادر تحت پوشش',
    'brother_under_coverage': 'برادر تحت پوشش',
    'sister_under_coverage': 'خواهر تحت پوشش',
    'only_child': 'تک فرزند',
    'only_son': 'تک فرزند ذکور',
    'divorced_child': 'فرزند طلاق',
    'family_support': 'کمک خرج خانواده',
    'father_sick': 'پدر بیمار',
    'mother_sick': 'مادر بیمار',
    'father_disabled': 'پدر از کار افتاده',
    'father_deceased': 'پدر متوفی',
    'mother_deceased': 'مادر متوفی',
    'need_declared': 'اعلام نیاز',
    'married': 'متاهل',
    'has_child': 'دارای فرزند',
    'description': 'توضیحات'
}

class SoldierFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='جستجو',
        widget=forms.TextInput(attrs={'placeholder': 'نام، نام خانوادگی یا کد ملی', 'class':'form-control'})
    )
    battalion_filter = forms.ChoiceField(
        required=False,
        label='گردان',
        choices=[],
        widget=forms.Select(attrs={'class':'form-control'})
    )
    group_filter = forms.ChoiceField(
        required=False,
        label='گروهان',
        choices=[],
        widget=forms.Select(attrs={'class':'form-control'})
    )

    def __init__(self, *args, **kwargs):
        battalions = kwargs.pop('battalions', [])
        groups = kwargs.pop('groups', [])
        super().__init__(*args, **kwargs)
        self.fields['battalion_filter'].choices = [('', 'انتخاب گردان')] + [(b.id, b.name) for b in battalions]
        self.fields['group_filter'].choices = [('', 'انتخاب گروهان')] + [(g.id, g.name) for g in groups]

class SoldierProblemForm(forms.Form):
    soldier_id = forms.IntegerField(widget=forms.HiddenInput())

    for field in PROBLEM_FIELDS:
        locals()[field] = forms.BooleanField(
            required=False, 
            label=PROBLEM_LABELS.get(field, field),
            widget=forms.CheckboxInput(attrs={
                'class': 'problem-checkbox'
            })
        )

    description = forms.CharField(required=False, label='توضیحات',     
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,  # دو خط
            'placeholder': 'توضیحات مشکلات سرباز را اینجا وارد کنید'
        })
    )
from django import forms
from soldiers.models import Soldier
from soldiers.constants import physical_condition_list, Type_of_disease_list
from django import forms
from soldiers.models import Soldier
from soldiers.constants import physical_condition_list, Type_of_disease_list

class TestSalamatRavanForm(forms.Form):
    soldier = forms.ModelChoiceField(
        queryset=Soldier.objects.all(),
        widget=forms.Select(attrs={'id':'soldier-select','class': 'form-control select2'}),
        label='انتخاب سرباز'
    )
    physical_condition_test = forms.ChoiceField(
        choices=physical_condition_list,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='تست سلامت روان'
    )
    physical_condition_description_test = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'توضیحات تست سلامت روان'}
        ),
        label='توضیحات تست سلامت روان',
        required=False
    )

    Type_of_disease_test = forms.ChoiceField(
        choices=Type_of_disease_list,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;',
                'data-tags': 'true',  # این اجازه تایپ و اضافه کردن گزینه جدید را می‌دهد
                'data-placeholder': 'انتخاب یا وارد کردن نوع بیماری'
            }
        ),
        label='نوع بیماری',
        required=False
    )
    # تاریخ آزمون (اختیاری، پیش‌فرض امروز)
    physical_condition_date_test = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='تاریخ آزمون',
        required=False
    )
