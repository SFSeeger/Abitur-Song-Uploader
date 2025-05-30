# Generated by Django 4.2.1 on 2023-05-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0002_answer_answer_value_id_answer_content_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="max_answers",
            field=models.PositiveSmallIntegerField(
                blank=True,
                default=1,
                help_text="Max amounts of Answers that can be given",
                verbose_name="Max Answers",
            ),
        ),
    ]
