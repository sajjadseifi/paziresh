from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from accounts.forms import LoginForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User


from django.shortcuts import render, redirect
from .models import AccessName, UserAccess,ApplicationValues,DepartmentValues
from django.contrib.auth.models import User
from battalions.models import battalion, battalion_group


from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm

def user_login_page(request, *args, **kwargs):
    print("=== ورود به صفحه لاگین ===")
    login_form = LoginForm(request.POST or None)
    print("POST data:", request.POST)
    
    if login_form.is_valid():
        print("فرم لاگین معتبر است ✅")
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        print("داده‌های فرم:", "username =", username, ", password =", password)
        
        user = User.objects.filter(username=username).first()
        print("کاربر پیدا شد؟", "بله" if user else "خیر")
        
        if user is None:
            print(f"کاربری با نام کاربری '{username}' وجود ندارد ❌")
            login_form = LoginForm(request.POST or None)
            return render(request, 'accounts/login_page.html', {'login_form': login_form})
        
        if user.check_password(password):
            print(f"رمز عبور برای کاربر '{username}' صحیح است ✅")
            login(request, user)
            return HttpResponseRedirect(reverse("home_page"))
        else:
            print(f"رمز عبور برای کاربر '{username}' نادرست ❌")
            return render(request, 'accounts/login_page.html', {'login_form': login_form})
    else:
        print("فرم لاگین معتبر نیست ❌")
        print("خطاهای فرم:", login_form.errors)

    return render(request, 'accounts/login_page.html', {'login_form': login_form})


def c_logout(request):
    logout(request)
    return redirect('home_page')



@user_passes_test(lambda u: u.is_staff)
@login_required
def account_access(request):
    if not request.user.is_staff:
        return redirect('home_page')

    # گرفتن user_id و tab از query string یا POST
    user_id = request.POST.get('user_id') or request.GET.get('user_id')
    tab = request.GET.get('tab', '')  # تب پیش‌فرض

    user = None
    user_access = []
    access_names = AccessName.choices()

    # پیدا کردن کاربر
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            user_access = user.accesses.all()
        except User.DoesNotExist:
            user = None
            user_access = []

    # اضافه کردن دسترسی جدید
    if request.method == "POST" and 'add_access' in request.POST:
        access_name = request.POST.get('access_name')
        access_value = request.POST.get('access_value', '')
        if user and access_name:
            UserAccess.objects.get_or_create(
                user=user,
                access_name=access_name,
                access_value=access_value
            )
        return redirect(f'?user_id={user.id}&tab={tab}')

    # حذف دسترسی
    if request.method == "POST" and 'remove_access' in request.POST:
        access_id = request.POST.get('access_id')
        UserAccess.objects.filter(id=access_id).delete()
        return redirect(f'?user_id={user.id}&tab={tab}')

    # اگر فقط کاربر انتخاب شود (radio button)
    if request.method == "POST" and 'user_id' in request.POST and not ('add_access' in request.POST or 'remove_access' in request.POST):
        return redirect(f'?user_id={user_id}&tab={tab}')

    # همه کاربران
    users = User.objects.all().order_by('-is_staff','username')

    # گردان‌ها و گروهان‌ها
    gordans = battalion.objects.all()
    grohans = battalion_group.objects.all()
    print(user_access)
    context = {
        'access_names': access_names,
        'application_values': ApplicationValues.choices(),
        'departments_values': DepartmentValues.choices(),
        'user_id': user_id,
        'user_access': user_access,
        'user': user,
        'users': users,
        'gordans': gordans,
        'grohans': grohans,
        'tab': tab,
    }

    return render(request, 'accounts/account_access.html', context)

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .forms import UserDetailsForm,NewUserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

@user_passes_test(lambda u: u.is_staff)
@login_required
def user_details_form(request):
    user_id = request.GET.get('user_id')
    current_tab = 'details'
    
    if not user_id:
        messages.error(request, "کاربری انتخاب نشده است.")
        return redirect('account_access')

    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        
        form = UserDetailsForm(request.POST, instance=user, request_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"اطلاعات کاربر {user.username} با موفقیت بروزرسانی شد ✅")
            return redirect(f"{reverse('account_access')}?user_id={user.id}&tab={current_tab}")
        else:
            # اگر فرم خطا داشت، می‌توانیم پیام خطا را نشان دهیم
            for field, errors in form.errors.items():
                for error in errors:
                    print(field,error)
                    messages.error(request, f"{field}: {error}")
    
    return redirect(f"{reverse('account_access')}?user_id={user_id}&tab={current_tab}")

@user_passes_test(lambda u: u.is_staff)
@login_required
def create_new_user_form(request):
    current_tab = request.GET.get('tab', '')  # تب پیش‌فرض
    user_id = request.GET.get('user_id', '')  # اگر کاربری قبلاً انتخاب شده بود

    print("Create New User")
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"کاربر {user.username} با موفقیت ایجاد شد ✅")
            return redirect(f"{reverse('account_access')}?user_id={user.id}&tab={current_tab}")
        else:
            # نمایش خطاهای فرم
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    if user_id:
        return redirect(f"{reverse('account_access')}?user_id={user_id}&tab={current_tab}")
    return redirect(f"{reverse('account_access')}?tab={current_tab}")



from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import ChangePasswordForm

@user_passes_test(lambda u: u.is_staff)
@login_required
def user_change_password_form(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        messages.error(request, "کاربری انتخاب نشده است.")
        return redirect('account_access')

    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, "کاربر یافت نشد.")
        return redirect('account_access')

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, f"رمز عبور کاربر {user.username} با موفقیت تغییر یافت ✅")
            return redirect(f"{reverse('account_access')}?user_id={user.id}&tab=password")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return redirect(f"{reverse('account_access')}?user_id={user.id}&tab=password")


from .forms import SoldiersAccessForm

@user_passes_test(lambda u: u.is_staff)
@login_required
def soldiers_access_form(request):
    user_id = request.GET.get('user_id')
    current_tab = 'soldiers'

    if not user_id:
        messages.error(request, "کاربری انتخاب نشده است.")
        return redirect(f"{reverse('account_access')}")

    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, "کاربر یافت نشد.")
        return redirect(f"{reverse('account_access')}?user_id=${user_id}&tab={current_tab}")

    grohans = battalion_group.objects.all()

    # دیکشنری دسترسی‌های کاربر برای پیش‌فرض فرم
    user_access = {int(ua.access_value): True for ua in user.accesses.filter(access_name=AccessName.GROHAN_SOLDIERS.name)}

    if request.method == "POST":
        form = SoldiersAccessForm(grohans, user_access, request.POST)
        if form.is_valid():
            # حذف دسترسی‌های قبلی
            UserAccess.objects.filter(user=user, access_name=AccessName.GROHAN_SOLDIERS.name).delete()
            # ایجاد دسترسی‌های جدید
            for field, value in form.cleaned_data.items():
                if value:  # فقط اگر تیک زده شده باشد
                    gr_id = int(field.replace('grohan_', ''))
                    UserAccess.objects.create(
                        user=user,
                        access_name=AccessName.GROHAN_SOLDIERS.name,
                        access_value=str(gr_id)
                    )
            messages.success(request, "دسترسی‌ها با موفقیت بروزرسانی شد ✅")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    # ریدایرکت به صفحه اصلی دسترسی‌ها در همه حالت
    return redirect(f"{reverse('account_access')}?user_id={user.id}&tab={current_tab}")


from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.urls import reverse
from .forms import FlexibleAccessForm
from .models import User

@user_passes_test(lambda u: u.is_staff)
@login_required
def application_access_form(request):
    user_id = request.GET.get('user_id')
    current_tab = 'applications'

    if not user_id:
        messages.error(request, "کاربری انتخاب نشده است.")
        return redirect(reverse('account_access'))

    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, "کاربر یافت نشد.")
        return redirect(f"{reverse('account_access')}?user_id={user_id}&tab={current_tab}")

    if request.method == 'POST':
        form = FlexibleAccessForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"دسترسی‌های کاربر {user.username} ذخیره شد ✅")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(error)
                    messages.error(request, f"{field}: {error}")

        # بعد از POST، redirect به تب applications
        return redirect(f"{reverse('account_access')}?user_id={user.id}&tab={current_tab}")

    # اگر GET بود، فقط redirect به صفحه حساب
    return redirect(f"{reverse('account_access')}?user_id={user.id}&tab={current_tab}")


def account_access_403(request):
    return render(request, 'errors/access_403_page.html')