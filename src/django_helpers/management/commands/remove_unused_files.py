import os
import sys
from datetime import datetime
from io import StringIO
from typing import Any, Optional

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        stdout_backup = sys.stdout
        sys.stdout = buf = StringIO()
        call_command("unreferenced_files")
        sys.stdout = stdout_backup
        data = buf.getvalue().strip().split("\n")
        for file in data:
            if not file == "":
                os.remove(file)
        return f"Removed {len(data)} file(s)"
