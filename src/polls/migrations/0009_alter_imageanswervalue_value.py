# Generated by Django 4.2.1 on 2023-06-04 14:53

from django.db import migrations
import pictures.models
import polls.models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0008_alter_question_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imageanswervalue",
            name="value",
            field=pictures.models.PictureField(
                aspect_ratios=[None, "1/1"],
                breakpoints={"l": 1200, "m": 992, "s": 768, "xl": 1400, "xs": 576},
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
    ]