from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import os


def generate_filename(self, filename):
    name = "%s/%s" % (self.user.id, os.path.basename(filename))
    return name


class Submission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    song_url = models.URLField(_("Song URL"), max_length=512, null=True)
    start_time = models.IntegerField(
        _("Start Time (in sec.)"),
        validators=[validators.MinValueValidator(0)],
        default=0,
    )
    end_time = models.IntegerField(
        _("End Time"),
        validators=[validators.MinValueValidator(1)],
        default=1,
    )

    song = models.FileField(
        _("Song File"),
        upload_to=generate_filename,
        validators=[validators.FileExtensionValidator(["mp3", "wav", "ogg"])],
        null=True,
    )
