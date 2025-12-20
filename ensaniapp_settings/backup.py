# utils/backup.py
import shutil
from pathlib import Path
import jdatetime
from ensaniapp_settings.models import EnsaniSettings

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUPS_DIR = BASE_DIR / "@bacckups"


def backup_sqlite_database_for_new_period():
    db_path = BASE_DIR / "db.sqlite3"

    if not db_path.exists():
        raise FileNotFoundError("db.sqlite3 not found")

    en = EnsaniSettings.objects.last()
    dore = en.shomare_dore if en else "unknown"

    time_str = jdatetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")

    # 📁 پوشه دوره
    period_dir = BACKUPS_DIR / dore
    period_dir.mkdir(parents=True, exist_ok=True)

    backup_filename = f"backup__{dore}__{time_str}.sqlite3"
    backup_path = period_dir / backup_filename

    shutil.copy2(db_path, backup_path)

    return backup_path
