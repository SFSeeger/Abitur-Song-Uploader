from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from pictures.models import PictureField

from songuploader.utils import generate_filename

# Create your models here.
class UserImage(models.Model):
    type_choices = ((0, _("Picture")), (1, _("Baby Picture")))

    image_type = models.IntegerField(_("Image Type"), choices=type_choices)

    user = models.ForeignKey(
        "auth.user", on_delete=models.CASCADE, verbose_name=_("User")
    )

    width = models.IntegerField()
    height = models.IntegerField()
    image = PictureField(
        _("Image"),
        upload_to=generate_filename,
        aspect_ratios=[None, "1/1", "15/16"],
        width_field="width",
        height_field="height",
    )
    description = models.CharField(_("description"), max_length=512)

    changed_at = models.DateTimeField(_("Changed at"), auto_now=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("User Image")
        verbose_name_plural = _("User Images")

    def __str__(self) -> str:
        return self.user.get_username()
