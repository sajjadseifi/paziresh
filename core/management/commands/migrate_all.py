from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path
import os

class Command(BaseCommand):
    help = "Run migrate on all databases including backups."

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        backup_dir = base_dir / "@bacckups"

        main_db = base_dir / "db.sqlite3"

        # 1. Migrate the main database
        self.stdout.write(self.style.SUCCESS(f"🏁 Starting migration on main database: {main_db.name}"))
        self.stdout.write(f" ➡️   Migrating: {main_db.name}")
        os.environ["DJANGO_DB_PATH_OVERRIDE"] = str(main_db)
        call_command("migrate", database="default")

        # 2. Migrate all SQLite backup files in @bacckups folder
        if not backup_dir.exists():
            self.stdout.write(self.style.WARNING("⚠️ Backup folder (@bacckups) not found."))
            return

        for db_path in backup_dir.glob("*.sqlite3"):
            self.stdout.write(f" ➡️   Migrating: {db_path.name}")
            os.environ["DJANGO_DB_PATH_OVERRIDE"] = str(db_path)
            call_command("migrate", database="default")

        self.stdout.write(self.style.SUCCESS("✅ Migration completed successfully for all databases."))
