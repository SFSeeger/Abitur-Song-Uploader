from django_q.tasks import async_task
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        msg = EmailMultiAlternatives(
            subject="Here are your Credentials",
            body=render_to_string("uploader/email/text/password_notification.txt", {}),
            to=["simon.f.seeger@gmx.de"],
            alternatives=[
                (
                    render_to_string(
                        "uploader/email/html/password_notification.html", {}
                    ),
                    "text/html",
                )
            ],
        )
        msg.send()
