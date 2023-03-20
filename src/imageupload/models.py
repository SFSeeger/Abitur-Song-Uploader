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

    image = PictureField(
        _("Image"),
        upload_to=generate_filename,
    )
    description = models.CharField(_("description"), max_length=512)

    changed_at = models.DateTimeField(_("Changed at"))
    created_at = models.DateTimeField(_("Created at"), auto_created=True)

    def save(self, *args, **kwargs) -> None:
        self.changed_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("User Image")
        verbose_name_plural = _("User Images")
