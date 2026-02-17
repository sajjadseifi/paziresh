import os
import sys
import subprocess
from datetime import datetime

# =====================
# کلاس چاپ رنگی و مرتب
# =====================
class Printer:
    COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }

    @staticmethod
    def print(msg, color="white", prefix=""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        pre = f"[{timestamp}] {prefix}\t" if prefix else f"[{timestamp}]\t\t"
        print(f"{Printer.COLORS.get(color,'')}{pre}{msg}{Printer.COLORS['reset']}")

# =====================
# تابع اجرای دستورات
# =====================
def run_command(cmd_list):
    """اجرای یک دستور به عنوان subprocess"""
    try:
        subprocess.run(cmd_list, check=True)
    except subprocess.CalledProcessError as e:
        Printer.print(f"Command failed: {e}", "red", "ERROR")
        sys.exit(1)

# =====================
# سوئیچ‌ها و فایل env
# =====================
MODE = "dev"
ENV_MAP = {
    "--dev": ".env.dev",
    "--prod": ".env.prod",
    "--deploy": ".env.prod",
    "--pre-deploy": ".env.prod",
    "--test": ".env.test"
}

for flag, env_file in ENV_MAP.items():
    if flag in sys.argv:
        MODE = flag[2:]  # فقط dev/prod/test/...
        SELECTED_ENV = env_file
        sys.argv.remove(flag)
        break
else:
    # حالت پیشفرض
    SELECTED_ENV = ".env.dev"

Printer.print(f"Mode: {MODE.upper()}", "cyan", "INFO")
Printer.print(f"Environment file: {SELECTED_ENV}", "cyan", "INFO")

# =====================
# بارگذاری env
# =====================
try:
    from dotenv import load_dotenv
except ImportError:
    Printer.print("python-dotenv not installed. Install with 'pip install python-dotenv'", "red", "ERROR")
    sys.exit(1)

if os.path.exists(SELECTED_ENV):
    load_dotenv(SELECTED_ENV)
    Printer.print(f"Environment loaded from {SELECTED_ENV}", "green", "INFO")
else:
    Printer.print(f"Environment file {SELECTED_ENV} not found. Using fallback defaults!", "yellow", "WARN")

# =====================
# مقادیر کلیدی
# =====================
DEBUG = os.getenv("DEBUG", "True")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*")
APP_SETTINGS =  os.getenv("APP_SETTINGS", "")

Printer.print(f"DEBUG = {DEBUG}", "yellow")
Printer.print(f"ALLOWED_HOSTS = {ALLOWED_HOSTS}", "yellow")

# =====================
# تنظیمات Django
# =====================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", APP_SETTINGS)
Printer.print(f"DJANGO_SETTINGS_MODULE = {os.environ['DJANGO_SETTINGS_MODULE']}", "green")

# =====================
# مسیر manage.py
# =====================
MANAGE_PY = os.path.join(os.getcwd(), "manage.py")

# =====================
# دستور دلخواه --cmd
# =====================
if "--cmd" in sys.argv:
    idx = sys.argv.index("--cmd")
    if len(sys.argv) > idx + 1:
        cmd = sys.argv[idx + 1]
        Printer.print(f"Running custom command: {cmd}", "magenta", "ACTION")
        run_command([sys.executable, MANAGE_PY, cmd])
        sys.exit(0)
    else:
        Printer.print("--cmd requires an argument", "red", "ERROR")
        sys.exit(1)

# =====================
# رفتار مستقل هر سوئیچ
# =====================
if MODE == "dev":
    Printer.print("Dev mode detected. Running runserver...", "magenta", "ACTION")
    run_command([sys.executable, MANAGE_PY, "runserver"])
    sys.exit(0)

elif MODE == "prod":
    Printer.print("Prod mode detected. Running migrate...", "magenta", "ACTION")
    run_command([sys.executable, MANAGE_PY, "runserver"])
    # run_command([sys.executable, MANAGE_PY, "migrate"])
    sys.exit(0)

elif MODE == "test":
    Printer.print("Test mode detected. Running tests...", "magenta", "ACTION")
    run_command([sys.executable, MANAGE_PY, "test"])
    sys.exit(0)

elif MODE == "deploy":
    Printer.print("Deploy mode detected. Running collectstatic...", "magenta", "ACTION")
    run_command([sys.executable, MANAGE_PY, "collectstatic", "--noinput"])
    sys.exit(0)

elif MODE == "pre-deploy":
    Printer.print("Pre-deploy mode detected. Running collectstatic + migrate...", "magenta", "ACTION")
    run_command([sys.executable, MANAGE_PY, "collectstatic", "--noinput"])
    run_command([sys.executable, MANAGE_PY, "migrate"])
    sys.exit(0)

# =====================
# help
# =====================
Printer.print("\nUsage: python devops.py [OPTIONS]\n", "white")
Printer.print("Options:", "cyan")
Printer.print("  --dev          Load .env.dev and runserver automatically", "white")
Printer.print("  --prod         Load .env.prod and run production tasks", "white")
Printer.print("  --test         Load .env.test and run test tasks", "white")
Printer.print("  --deploy       Load .env.prod and run collectstatic", "white")
Printer.print("  --pre-deploy   Load .env.prod and run collectstatic + migrate", "white")
Printer.print("  --cmd CMD      Run a custom Django command CMD", "white")
Printer.print("  --help         Show this help message", "white")
sys.exit(0)
