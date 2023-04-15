import os
import tarfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        Path(settings.MEDIA_BACKUP_DIR).mkdir(parents=True, exist_ok=True)
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
