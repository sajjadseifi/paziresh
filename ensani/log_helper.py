from .models import ActivityLog
from django.utils import timezone


def log_activity(note_type, action, description=""):
    """
    تابع عمومی برای ثبت لاگ
    """
    log =  ActivityLog.objects.create(
        note_type=note_type,
        action=action,
        description=description,
        created_at=timezone.now() 
    )
    log.save()
    return log

# =======================
# User logs
# =======================
def log_user_create(target_user):
    return log_activity(
        note_type=ActivityLog.NoteType.USER,
        action=ActivityLog.Action.CREATE,
        description=f"ایجاد کاربر {target_user.username}"
    )

def log_user_update(target_user):
    return log_activity(
        note_type=ActivityLog.NoteType.USER,
        action=ActivityLog.Action.UPDATE,
        description=f"ویرایش کاربر {target_user.username}"
    )

def log_user_delete(target_user):
    return log_activity(
        note_type=ActivityLog.NoteType.USER,
        action=ActivityLog.Action.DELETE,
        description=f"حذف کاربر {target_user.username}"
    )

# =======================
# Soldier logs
# =======================
def log_soldier_create(soldier):
    return log_activity(
        note_type=ActivityLog.NoteType.SOLDIER,
        action=ActivityLog.Action.CREATE,
        description=f"افزودن سرباز {soldier.name} {soldier.family}"
    )

def log_soldier_update(soldier):
    return log_activity(
        note_type=ActivityLog.NoteType.SOLDIER,
        action=ActivityLog.Action.UPDATE,
        description=f"ویرایش سرباز {soldier.name} {soldier.family}"
    )

def log_soldier_delete(soldier):
    return log_activity(
        note_type=ActivityLog.NoteType.SOLDIER,
        action=ActivityLog.Action.DELETE,
        description=f"حذف سرباز {soldier.name} {soldier.family}"
    )

# =======================
# Letter logs
# =======================
def log_letter_create(letter):
    return log_activity(
        note_type=ActivityLog.NoteType.LETTER,
        action=ActivityLog.Action.CREATE,
        description=f"ایجاد نامه با شماره {letter.number}"
    )

def log_letter_update(letter):
    return log_activity(
        note_type=ActivityLog.NoteType.LETTER,
        action=ActivityLog.Action.UPDATE,
        description=f"ویرایش نامه با شماره {letter.number}"
    )

def log_letter_delete(letter):
    return log_activity(
        note_type=ActivityLog.NoteType.LETTER,
        action=ActivityLog.Action.DELETE,
        description=f"حذف نامه با شماره {letter.number}"
    )

def log_letter_print(letter):
    return log_activity(
        note_type=ActivityLog.NoteType.LETTER,
        action=ActivityLog.Action.PRINT,
        description=f"پرینت نامه با شماره {letter.number}"
    )

def log_letter_status_change(letter, old_status, new_status):
    return log_activity(
        note_type=ActivityLog.NoteType.LETTER,
        action=ActivityLog.Action.STATUS_CHANGE,
        description=f"تغییر وضعیت نامه {letter.number} از '{old_status}' به '{new_status}'"
    )

# =======================
# System logs
# =======================
def log_system_event(description):
    return log_activity(
        note_type=ActivityLog.NoteType.SYSTEM,
        action=ActivityLog.Action.UPDATE,
        description=f"سیستم: {description}"
    )

def log_system_error(description):
    return log_activity(
        note_type=ActivityLog.NoteType.SYSTEM,
        action=ActivityLog.Action.STATUS_CHANGE,
        description=f"خطای سیستم: {description}"
    )
