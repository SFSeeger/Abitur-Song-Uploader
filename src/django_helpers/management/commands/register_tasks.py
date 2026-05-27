from datetime import datetime
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule


class Command(BaseCommand):
    help = "Registers tasks specified in CRON_TASKS setting"

    def add_arguments(self, parser) -> None:
        parser.add_argument("option", type=str, choices=["register", "remove"])
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "-a", action="store_true", help="(Un)Registers all tasks"
        )
        group.add_argument(
            "-t",
            type=str,
            nargs="+",
            action="append",
            help="Selects certain tasks to register",
        )

    def create_schedule(self, key, value):
        dtime = datetime.strptime(value["run_at"], "%H:%M")
        if type(value["args"]) == str:
            value["args"] = [value["args"]]
        schedule(
            value.get("func", "django.core.management.call_command"),
            *value["args"],
            name=value.get("name", key),
            q_options=value.get("q_options", {}),
            schedule_type=value["schedule_type"],
            next_run=datetime.now().replace(hour=dtime.hour, minute=dtime.minute),
            repeats=-1,
        )

    def handle(self, **options: Any) -> str | None:
        if options["option"] == "register":
            if options.get("a"):
                Schedule.objects.all().delete()
                for key, value in settings.CRON_TASKS.items():
                    self.create_schedule(key, value)
            elif tasks := options.get("t"):
                for task in tasks:
                    self.create_schedule(task, settings.CRON_TASKS[task])
            return f"Tasks created"

        elif options["option"] == "remove":
            if options.get("a"):
                Schedule.objects.all().delete()
            elif tasks := options.get("t"):
                Schedule.objects.filter(name__in=tasks).delete()
            return "Tasks removed"
        return None
