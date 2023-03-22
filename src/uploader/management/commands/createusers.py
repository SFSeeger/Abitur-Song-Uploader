import argparse
import random
import string

import pandas as pd
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django_q.tasks import async_task
from tqdm import tqdm

pool = string.ascii_letters + string.digits


def generate_password() -> str:
    return "".join(random.choice(pool) for i in range(6))


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
            password = generate_password()
            first_name = row["first_name"]
            last_name = row["last_name"]
            email = row["email"]
            username = first_name + last_name
            username = username.replace(".", "").replace(" ", "").lower()

            if not (user := User.objects.filter(username=username)):
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    **row,
                )
                user.save()
            elif user.first().last_login == None:
                user = user.first()
                user.email = email
                user.password = generate_password()
                user.save()
            else:
                continue
            context = {
                "first_name": first_name,
                "username": username,
                "password": password,
                "public_domain": settings.PUBLIC_DOMAIN,
            }
            async_task(
                "django.core.mail.send_mail",
                "Here are your Credentials",
                render_to_string(
                    "uploader/email/text/password_notification.txt", context
                ),
                None,
                recipient_list=[user.email],
                html_message=render_to_string(
                    "uploader/email/html/credentials.html", context
                ),
            )
