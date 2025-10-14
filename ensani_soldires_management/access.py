from battalions.models import battalion, battalion_group
from soldiers.models import Soldier
from accounts.models import UserAccess, AccessName


def get_user_battalions(user):
    """
    برمی‌گرداند گردان‌هایی که کاربر اجازه مشاهده دارد.
    حتی اگر فقط به یک گروهان دسترسی داشته باشد، گردان مربوطه نیز داده می‌شود.
    """
    if not user.is_authenticated:
        return battalion.objects.none()

    if user.is_staff:
        return battalion.objects.all()

    # دسترسی مستقیم به گردان
    gordan_access = UserAccess.objects.filter(
        user=user,
        access_name=AccessName.GORDAN_SOLDIERS.name
    )
    battalion_ids = [int(a.access_value) for a in gordan_access if a.access_value.isdigit()]

    # دسترسی غیرمستقیم از گروهان‌ها
    group_access = UserAccess.objects.filter(
        user=user,
        access_name=AccessName.GROHAN_SOLDIERS.name
    )
    group_ids = [int(a.access_value) for a in group_access if a.access_value.isdigit()]
    
    # گردان‌هایی که گروهان‌ها به آن تعلق دارند
    battalion_ids_from_groups = list(
        battalion_group.objects.filter(id__in=group_ids)
        .values_list('gordan__id', flat=True)
    )

    # ادغام دسترسی مستقیم و غیرمستقیم
    all_battalion_ids = list(set(battalion_ids + battalion_ids_from_groups))

    return battalion.objects.filter(id__in=all_battalion_ids)


# 2️⃣ تابع دریافت گروهان‌ها بر اساس دسترسی کاربر
def get_user_battalion_groups(user):
    """
    گروهان‌هایی که کاربر اجازه دسترسی دارد را برمی‌گرداند.
    اگر کاربر به کل گردان دسترسی داشته باشد، گروهان‌های آن گردان نیز بازگردانده می‌شوند.
    """
    if not user.is_authenticated:
        return battalion_group.objects.none()

    if user.is_staff:
        return battalion_group.objects.all()

    # دسترسی مستقیم به گروهان
    group_access = UserAccess.objects.filter(user=user, access_name=AccessName.GROHAN_SOLDIERS.name)
    if group_access.filter(access_value='همه').exists():
        return battalion_group.objects.all()

    group_ids = [int(a.access_value) for a in group_access if a.access_value.isdigit()]

    # گروهان‌هایی که از گردان‌های مجاز هستند
    battalions_allowed = get_user_battalions(user)
    groups_from_battalion = battalion_group.objects.filter(gordan__in=battalions_allowed)

    return battalion_group.objects.filter(id__in=group_ids) | groups_from_battalion


# 3️⃣ تابع دریافت سربازان بر اساس دسترسی کاربر
def get_user_soldiers(user):
    """
    سربازانی که کاربر اجازه مشاهده دارد.
    بر اساس دسترسی به گردان و گروهان فیلتر می‌شود.
    """
    if not user.is_authenticated:
        return Soldier.objects.none()

    if user.is_staff:
        return Soldier.objects.all()

    battalions_allowed = get_user_battalions(user)
    battalion_groups_allowed = get_user_battalion_groups(user)

    return Soldier.objects.filter(
        Gordan__in=battalions_allowed
    ) | Soldier.objects.filter(
        battalion_group__in=battalion_groups_allowed
    )
