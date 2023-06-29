from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_q.tasks import async_chain, async_task

User = get_user_model()


class Command(BaseCommand):
    help = "To manually redownload/slice songs for users"

    def handle(self, *args, **options):
        users = User.objects.filter(submission=None).prefetch_related("submission_set")
        context = {
            "domain": settings.BASE_URL,
            "protocol": "https",
        }
        for user in users:
            context["user"] = user
            message = mail.EmailMultiAlternatives(
                subject="Don't Forget to Submit Your Song for the Graduation Ceremony!",
                body=render_to_string(
                    "uploader/email/text/song_reminder.txt", context=context
                ),
                to=[user.email],
            )
            message.attach_alternative(
                render_to_string(
                    "uploader/email/html/song_reminder.html", context=context
                ),
                "text/html",
            )
            async_task(message.send())
        return f"Notified {users.count()} Users"
