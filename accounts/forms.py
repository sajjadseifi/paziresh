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
