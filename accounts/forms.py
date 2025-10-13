from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'id': 'username',
                   'placeholder': 'نام کاربری وارد کنید'}),
        label='ایمیل',

    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'type': 'password', 'id': 'password', 'class': 'form-control', 'name': 'password',
                   'placeholder': 'رمز عبور را وارد کنید', 'required': "ایمیل خود را وارد کنید"}),
        label='رمز عبور'
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        if is_exists_user is False:
            raise forms.ValidationError('کاربری با این نام ثبت ثبت نشده')
        return user_name

    def clean_password(self):
        if len(self.cleaned_data.get('password')) < 4:
            raise forms.ValidationError("رمز عبور وارد شده کمتر از 4 کارکتر می باشد")
        return self.cleaned_data.get('password')


from django import forms
from django.contrib.auth.models import User

class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff']

    def __init__(self, *args, **kwargs):
        # دریافت کاربر جاری برای جلوگیری از تغییر is_staff خودش
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        
        # اگر کاربر خودش را ویرایش می‌کند، تیک ادمینی را غیرقابل تغییر می‌کنیم
        if self.instance and self.request_user and self.instance.id == self.request_user.id:
            self.fields['is_staff'].disabled = True
            self.fields['is_staff'].help_text = "شما نمی‌توانید دسترسی ادمین خود را تغییر دهید."

    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
        if not username:
            raise forms.ValidationError("نام کاربری نمی‌تواند خالی باشد.")
        
        # بررسی یونیک بودن نام کاربری (به جز خودش)
        qs = User.objects.filter(username=username)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("این نام کاربری قبلاً استفاده شده است.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip()
        return email


from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class NewUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        min_length=4,
        help_text="رمز عبور باید حداقل 4 کاراکتر باشد."
    )
    is_staff = forms.BooleanField(
        required=False,
        label="ادمین"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'مثلاً علی'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'مثلاً رضایی'}),
            'username': forms.TextInput(attrs={'placeholder': 'مثلاً alirez'}),
            'email': forms.EmailInput(attrs={'placeholder': 'مثلاً example@mail.com'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("این نام کاربری قبلاً استفاده شده است.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً استفاده شده است.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # هش کردن پسورد
        if commit:
            user.save()
        return user



class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="گذرواژه",
        min_length=4,
        required=True
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="تایید گذرواژه",
        min_length=4,
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("رمز عبور و تایید آن مطابقت ندارند.")
        return cleaned_data
    
    
from django import forms

class SoldiersAccessForm(forms.Form):
    """
    فرم داینامیک برای مدیریت دسترسی‌ها به گروهان‌ها
    """
    def __init__(self, grohans, user_access=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_access = user_access or {}
        
        for gr in grohans:
            field_name = f'grohan_{gr.id}'
            self.fields[field_name] = forms.BooleanField(
                label=f'گروهان {gr.name}',
                required=False,
                initial=self.user_access.get(gr.id, False)
            )


# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserAccess, AccessName, ApplicationValues, DepartmentValues
import logging

logger = logging.getLogger(__name__)

class FlexibleAccessForm(forms.Form):
    """
    فرم واحد برای مدیریت دسترسی‌ها:
    - ApplicationValues
    - DepartmentValues
    خودش تشخیص می‌دهد چه دسترسی‌هایی باید ساخته شوند.
    """

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # ترکیب همه گزینه‌ها: (access_name, choices_list)
        self.access_groups = [
            (AccessName.APPLICATIONS, ApplicationValues.choices()),
            (AccessName.DEPARTMENTS, DepartmentValues.choices())
        ]

        # ساخت فیلدها
        for access_name, choices_list in self.access_groups:
            for key, value in choices_list:
                field_name = f"{access_name.name.lower()}_{key}"
                initial = False
                if user:
                    initial = UserAccess.objects.filter(
                        user=user,
                        access_name=access_name.name,
                        access_value=key
                    ).exists()

                self.fields[field_name] = forms.BooleanField(
                    required=False,
                    label=value,
                    initial=initial
                )

    def save(self):
        if not self.user:
            raise ValueError("کاربر مشخص نشده است!")

        for access_name, choices_list in self.access_groups:
            print(f"[FlexibleAccessForm] Saving for user: {self.user.username} | AccessName: {access_name.name}")

            # حذف دسترسی‌های قبلی برای این access_name
            deleted_count, _ = UserAccess.objects.filter(
                user=self.user,
                access_name=access_name.name
            ).delete()
            print(f"[FlexibleAccessForm] Deleted {deleted_count} old access entries for {access_name.name}")

            # افزودن موارد انتخاب‌شده
            for key, _ in choices_list:
                field_name = f"{access_name.name.lower()}_{key}"
                value = self.cleaned_data.get(field_name)
                print(f"[FlexibleAccessForm] Field: {field_name} = {value}")
                if value:
                    ua = UserAccess.objects.create(
                        user=self.user,
                        access_name=access_name.name,
                        access_value=key
                    )
                    print(f"[FlexibleAccessForm] Created access: {ua}")
