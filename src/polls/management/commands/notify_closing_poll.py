import datetime
from typing import Any, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from tqdm import tqdm

from polls.models import Poll


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--timediff",
            type=int,
            default=5,
            help="Amount of days the notification will take place",
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        User = get_user_model()
        curr_time = datetime.datetime.now()
        check_date = curr_time + datetime.timedelta(days=options["timediff"])

        polls = Poll.objects.filter(end_date=check_date)
        mails = []
        for poll in polls:
            diff = set(User.objects.all().values_list("id", flat=True)) - set(
                poll.response_set.all().values_list("user", flat=True)
            )

            users = User.objects.filter(id__in=diff)
            user_count = users.count()
            context = {
                "public_domain": settings.PUBLIC_DOMAIN,
                "poll": poll,
                "timediff": options["timediff"],
            }
            for user in tqdm(users, total=user_count):
                context["first_name"] = user.first_name
                message = mail.EmailMultiAlternatives(
                    subject="Reminder: Poll closing in %s days" % options["timediff"],
                    body=render_to_string(
                        "polls/email/text/poll_reminder.txt", context=context
                    ),
                    to=[user.email],
                )
                message.attach_alternative(
                    render_to_string(
                        "polls/email/html/poll_reminder.html", context=context
                    ),
                    "text/html",
                )
                mails.append(message)
        connection = mail.get_connection()
        connection.send_messages(mails)
