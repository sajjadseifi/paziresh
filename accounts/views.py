from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.forms import LoginForm


def user_login_page(request, *args, **kwargs):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = User.objects.filter(username=username).first()
        if user is None:
            login_form = LoginForm(request.POST or None)
            cx = {'login_form': login_form, }
            return render(request, 'accounts/login_page.html', cx)
        if user.check_password(password) is True:
            login(request, user)
            return render(request, 'ensani/panel_home_page.html')
        else:
            cx = {'login_form': login_form, }
            return render(request, 'accounts/login_page.html', cx)

    return render(request, 'accounts/login_page.html', context={'login_form': login_form, })
