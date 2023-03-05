from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


def generate_filename(self, filename):
    name = "uploads/%s" % (self.user.get_username())
    return name


class Submission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    song_url = models.CharField(_("Song URL"), max_length=512)
    start_time = models.IntegerField(_("Start Time"), blank=True, default=0)

    song = models.FileField(_("Song File"), upload_to=generate_filename)
