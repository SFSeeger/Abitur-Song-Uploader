# Generated by Django 4.1.7 on 2023-03-07 19:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("uploader", "0002_alter_submission_song_alter_submission_song_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="end_time",
            field=models.IntegerField(
                blank=True,
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="End Time",
            ),
        ),
    ]
