import argparse
import pandas as pd
from tqdm import tqdm
import random
import string

from django_q.tasks import async_task
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

pool = string.ascii_letters + string.digits


class Command(BaseCommand):
    help = "Creates users an sends them their passwords"

    def add_arguments(self, parser):
        parser.add_argument(
            "csvfile",
            type=str,
            help="The file containing all user data",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        df = pd.read_csv(options.get("csvfile"), delimiter=";")
        for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
            password = "".join(random.choice(pool) for i in range(6))
            first_name = row["first_name"]
            last_name = row["last_name"]
            email = row["email"]
            username = first_name + last_name
            username = username.strip(".").replace(" ", "").lower()

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    **row,
                )
                user.save()
            context = {
                "first_name": first_name,
                "username": username,
                "password": password,
                "public_domain": settings.PUBLIC_DOMAIN,
            }

            msg = EmailMultiAlternatives(
                subject="Here are your Credentials",
                body=render_to_string(
                    "uploader/email/text/password_notification.txt",
                    context,
                ),
                to=[user.email],
                alternatives=[
                    (
                        render_to_string(
                            "uploader/email/html/credentials.html",
                            context,
                        ),
                        "text/html",
                    )
                ],
            )
            msg.send()
