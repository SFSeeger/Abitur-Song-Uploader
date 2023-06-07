import datetime
import smtplib
import time
from typing import Any, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from tqdm import tqdm

from polls.utils import get_user_polls


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--timediff",
            type=int,
            default=5,
            help="Amount of days the notification will take place",
        )

        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Skips confirmation input",
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        User = get_user_model()
        curr_time = datetime.datetime.now()
        check_date = curr_time + datetime.timedelta(days=options["timediff"])

        users = User.objects.all()
        context = {
            "timediff": options["timediff"],
            "domain": settings.BASE_URL,
            "protocol": "https",
        }
        if not options["no_input"]:
            if (
                not input(f"Do you want to {users.count()} users? [yes/no] ")
                .lower()
                .strip()
                == "yes"
            ):
                return "Canceled"

        connection = mail.get_connection()

        failure = 0
        failure_users = []
        for idx, user in enumerate(tqdm(users, total=users.count())):
            polls = get_user_polls(user).filter(end_date=check_date)
            if (count := polls.count()) == 0:
                continue
            context["first_name"] = user.first_name
            context["polls"] = polls
            context["poll_count"] = count

            message = mail.EmailMultiAlternatives(
                subject=_("Reminder: %(poll_count)s Poll closing in %(timediff)s days")
                % context,
                body=render_to_string(
                    "polls/email/text/poll_reminder.txt", context=context
                ),
                to=[user.email],
                connection=connection,
            )
            message.attach_alternative(
                render_to_string(
                    "polls/email/html/poll_reminder.html", context=context
                ),
                "text/html",
            )
            if idx % 25 == 0:
                time.sleep(3)
            for i in range(15):
                try:
                    message.send()
                    break
                except (
                    smtplib.SMTPServerDisconnected,
                    smtplib.SMTPConnectError,
                ) as e:
                    connection = mail.get_connection()
                    connection.open()
                except (
                    smtplib.SMTPSenderRefused,
                    smtplib.SMTPRecipientsRefused,
                ) as e:
                    failure_users.append(user.get_username())
            else:
                failure += 1
        connection.close()
        return f"{users.count()-failure}/{users.count()} Emails successfully send! Missing: {failure_users}"
