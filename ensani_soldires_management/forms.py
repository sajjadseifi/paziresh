from django import forms
from soldiers.constants import PROBLEM_FIELDS,PROBLEM_LABELS


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
        self.fields['group_filter'].choices = [('', 'انتخاب گروهان')] + [(g.id, f'{g.gordan.name} (گروهان {g.name})') for g in groups]

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
            'rows': 2, 
            'style':'resize:none;',
            'placeholder': 'توضیحات مشکلات سرباز را اینجا وارد کنید',
        }),
        initial='',
        empty_value='',
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


# forms.py
from django import forms
from .models import IdeologicalAssessment
from django.core.exceptions import ValidationError
from django.forms.forms import NON_FIELD_ERRORS

class IdeologicalAssessmentForm(forms.ModelForm):
    class Meta:
        model = IdeologicalAssessment
        fields = ['rank', 'full_name']


class IdeologicalAssessmentBulkForm(forms.Form):
    SCORE_FIELDS = {
        "ideological_score_start",
        "ideological_score",
        "ideological_score_end",
        "quran_memorization",
    }

    ASSESSMENT_FIELDS = {
        "ideological_score_start_assessment",
        "ideological_score_assessment",
        "ideological_score_end_assessment",
    }

    CHECKBOX_FIELDS = {
        "nahj_memorization",
        "sajjadiya_memorization",
    }

    MAX_ASSESSOR_LENGTH = 255

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soldier_ids = set()
        self.cleaned_bulk_data = {}

        if self.data:
            self._extract_soldier_ids()

    def _extract_soldier_ids(self):
        """شناسایی آیدی سربازها از کلیدهای POST"""
        for key in self.data.keys():
            if "_" in key:
                sid = key.split("_")[0]
                if sid.isdigit():
                    self.soldier_ids.add(int(sid))

    def clean(self):
        cleaned = {}
        errors = []

        for key, value in self.data.items():
            if "_" not in key:
                continue

            sid_str, field = key.split("_", 1)
            if not sid_str.isdigit():
                continue
            sid = int(sid_str)

            # فیلدهای نمره‌ای → float
            if field in self.SCORE_FIELDS:
                try:
                    cleaned.setdefault(sid, {})[field] = float(value or 0.0)
                except (ValueError, TypeError):
                    errors.append(f"{key}: نمره معتبر نیست")

            # فیلدهای ارزیاب → رشته کوتاه
            elif field in self.ASSESSMENT_FIELDS:
                assessor = str(value).strip() if value else ""
                if len(assessor) > self.MAX_ASSESSOR_LENGTH:
                    errors.append(f"{key}: نام ارزیاب بیش از {self.MAX_ASSESSOR_LENGTH} کاراکتر است")
                else:
                    cleaned.setdefault(sid, {})[field] = assessor

            # checkbox → True اگر وجود داشته باشد
            elif field in self.CHECKBOX_FIELDS:
                cleaned.setdefault(sid, {})[field] = True

        # checkbox‌هایی که ارسال نشده → False
        for sid in self.soldier_ids:
            for field in self.CHECKBOX_FIELDS:
                if field not in cleaned.get(sid, {}):
                    cleaned.setdefault(sid, {})[field] = False

        if errors:
            raise ValidationError({forms.NON_FIELD_ERRORS: errors})

        self.cleaned_bulk_data = cleaned
        return cleaned




class BulkDynamicForm(forms.Form):
    INT_FIELDS = set()
    FLOAT_FIELDS = set()
    STRING_FIELDS = set()
    CHECKBOX_FIELDS = set()
    MAX_STRING_LENGTH = 255

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soldier_ids = set()
        self.cleaned_bulk_data = {}  # {sid: {field: value}}

        if self.data:
            self._extract_soldier_ids()

    def _extract_soldier_ids(self):
        for key in self.data.keys():
            if "_" in key:
                sid = key.split("_")[0]
                if sid.isdigit():
                    self.soldier_ids.add(int(sid))

    def clean(self):
        cleaned = {}
        errors = []

        for key, value in self.data.items():
            if "_" not in key:
                continue
            sid_str, field = key.split("_", 1)
            if not sid_str.isdigit():
                continue
            sid = int(sid_str)

            # convert empty string to None
            value = value if value not in ("", " ") else None

            if field in self.INT_FIELDS:
                if value is not None:
                    try:
                        cleaned.setdefault(sid, {})[field] = int(value)
                    except (ValueError, TypeError):
                        errors.append(f"{key}: مقدار صحیح معتبر نیست")
                else:
                    cleaned.setdefault(sid, {})[field] = None

            elif field in self.FLOAT_FIELDS:
                if value is not None:
                    try:
                        cleaned.setdefault(sid, {})[field] = float(value)
                    except (ValueError, TypeError):
                        errors.append(f"{key}: مقدار اعشاری معتبر نیست")
                else:
                    cleaned.setdefault(sid, {})[field] = None

            elif field in self.STRING_FIELDS:
                if value is not None:
                    val = str(value).strip()
                    if len(val) > self.MAX_STRING_LENGTH:
                        errors.append(f"{key}: طول رشته بیش از {self.MAX_STRING_LENGTH} کاراکتر است")
                    else:
                        cleaned.setdefault(sid, {})[field] = val
                else:
                    cleaned.setdefault(sid, {})[field] = None

            elif field in self.CHECKBOX_FIELDS:
                cleaned.setdefault(sid, {})[field] = bool(value)

        # checkbox هایی که ارسال نشده → False
        for sid in self.soldier_ids:
            for field in self.CHECKBOX_FIELDS:
                if field not in cleaned.get(sid, {}):
                    cleaned.setdefault(sid, {})[field] = False

        if errors:
            raise ValidationError({"__all__": errors})

        self.cleaned_bulk_data = cleaned
        return cleaned
