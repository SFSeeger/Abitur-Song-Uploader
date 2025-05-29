import os
import tarfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--keep",
            type=int,
            default=None,
            help="Number of backup files to keep. If not specified, all backups will be kept.",
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        Path(settings.MEDIA_BACKUP_DIR).mkdir(parents=True, exist_ok=True)
        keep = options.get("keep")
        if keep is not None:
            if keep < 0:
                raise CommandError("The --keep option must be a non-negative integer.")
            self._delete_old_backups(Path(settings.MEDIA_BACKUP_DIR), keep)

        file_path = (
            settings.MEDIA_BACKUP_DIR
            + datetime.now().strftime("%m%d%Y_%H%M%S")
            + ".tar.gz"
        )
        with tarfile.open(
            file_path,
            "w:gz",
        ) as tar:
            tar.add(settings.MEDIA_ROOT, arcname="media")
        return f"Backup saved: {file_path}"

    def _delete_old_backups(self, backup_dir: Path, keep: int):
        backups = sorted(backup_dir.glob("*.tar.gz"), key=lambda f: f.stat().st_mtime, reverse=True)
        for old_backup in backups[keep:]:
            old_backup.unlink()