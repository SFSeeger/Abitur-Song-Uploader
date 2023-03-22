from typing import Any, Optional
from tqdm import tqdm

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core import mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        User = get_user_model()
        users = User.objects.filter(vote=None)
        mails = []
        context = {
            "public_domain": settings.PUBLIC_DOMAIN,
        }
        for user in tqdm(users, total=users.count()):
            context["first_name"] = user.first_name
            message = mail.EmailMultiAlternatives(
                subject="Final Reminder: Vote for Themed Week in the Next 24 Hours",
                body=render_to_string(
                    "voting/email/text/vote_reminder.txt", context=context
                ),
                to=[user.email],
            )
            message.attach_alternative(
                render_to_string(
                    "voting/email/html/vote_reminder.html", context=context
                ),
                "text/html",
            )
            mails.append(message)
        connection = mail.get_connection()
        connection.send_messages(mails)
