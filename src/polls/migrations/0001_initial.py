# Generated by Django 4.2.1 on 2023-05-15 20:19

import django.db.models.deletion
import pictures.models
from django.conf import settings
from django.db import migrations, models

import polls.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CharAnswerValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=512, verbose_name="Value")),
            ],
        ),
        migrations.CreateModel(
            name="ImageAnswerValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
                (
                    "value",
                    pictures.models.PictureField(
                        aspect_ratios=[None, "1/1", "3/4"],
                        breakpoints={
                            "l": 1200,
                            "m": 992,
                            "s": 768,
                            "xl": 1400,
                            "xs": 576,
                        },
                        container_width=1200,
                        file_types=["WEBP"],
                        grid_columns=12,
                        height_field="height",
                        pixel_densities=[1, 2],
                        upload_to=polls.models.generate_poll_filename,
                        verbose_name="Image",
                        width_field="width",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="Name")),
                (
                    "description",
                    models.CharField(max_length=512, verbose_name="Description"),
                ),
                (
                    "start_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Start Date"),
                ),
                ("end_date", models.DateTimeField(verbose_name="End Date")),
                (
                    "can_answered_multiple",
                    models.BooleanField(verbose_name="Can be answered multiple times"),
                ),
            ],
            options={
                "verbose_name": "Poll",
                "verbose_name_plural": "Polls",
                "ordering": ["-end_date"],
                "permissions": [
                    ("can_open_polls", "Can open Polls"),
                    ("can_close_polls", "Can close Polls"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Response",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "poll",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polls.poll",
                        verbose_name="Poll",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question_type",
                    models.IntegerField(
                        choices=[
                            (0, "Text Type"),
                            (1, "Image Type"),
                            (2, "Multiple Choice Type"),
                        ],
                        verbose_name="Question Type",
                    ),
                ),
                (
                    "position",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Order in which questions are displayed",
                        verbose_name="Position",
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="Name")),
                (
                    "description",
                    models.CharField(max_length=512, verbose_name="Description"),
                ),
                (
                    "poll",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polls.poll",
                        verbose_name="Poll",
                    ),
                ),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
                "ordering": ["position"],
            },
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="Name")),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polls.question",
                        verbose_name="Question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Option",
                "verbose_name_plural": "Options",
            },
        ),
        migrations.CreateModel(
            name="MultipleChoiceAnswerValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "value",
                    models.ManyToManyField(to="polls.option", verbose_name="Values"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polls.question",
                        verbose_name="Question",
                    ),
                ),
                (
                    "response",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polls.response",
                        verbose_name="Response",
                    ),
                ),
            ],
        ),
    ]
