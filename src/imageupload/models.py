from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from pictures.models import PictureField

from songuploader.utils import generate_filename


class Profile(models.Model):
    user = models.ForeignKey(
        "auth.User", verbose_name=_("User"), on_delete=models.CASCADE
    )

    motto = models.CharField(
        max_length=128, verbose_name=_("My Motto"), null=True, blank=True
    )
    favorite_teacher = models.CharField(
        max_length=64, verbose_name=_("Favorite Teacher"), null=True, blank=True
    )
    favorite_subject = models.CharField(
        max_length=64, verbose_name=_("Favorite Subject"), null=True, blank=True
    )

    things_missed = models.CharField(
        _("Things I will miss"), max_length=256, null=True, blank=True
    )
    things_not_missed = models.CharField(
        _("Things I will not miss"), max_length=256, null=True, blank=True
    )
    cant_live_without = models.CharField(
        _("Things I can't live without"), max_length=256, null=True, blank=True
    )
    expulsion = models.CharField(
        _("Expulsions ans why"), max_length=128, null=True, blank=True
    )
    favorite_song = models.CharField(
        _("Favorite Song"), max_length=64, null=True, blank=True
    )
    celebrity_crush = models.CharField(
        _("Celebrity Crush"), max_length=32, null=True, blank=True
    )
    lower_level_crush = models.CharField(
        _("Lower Level Crush"), max_length=32, null=True, blank=True
    )

    best_school_experience = models.CharField(
        _("Best School Experience"), max_length=64, null=True, blank=True
    )
    worst_school_experience = models.CharField(
        _("Worst School Experience"), max_length=64, null=True, blank=True
    )

    school_thing_needed = models.CharField(
        _("Without that I would not have survived the school"),
        max_length=64,
        null=True,
        blank=True,
    )

    abi_learned = models.CharField(
        _("This is what I learned during my Abi"), max_length=64, null=True, blank=True
    )
    after_abi = models.CharField(
        _("What I will do after graduation"), max_length=128, null=True, blank=True
    )

    additional_info = models.CharField(
        _("Additional Info"), max_length=512, null=True, blank=True
    )


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
        aspect_ratios=[None, "1/1", "3/4"],
        width_field="width",
        height_field="height",
    )

    changed_at = models.DateTimeField(_("Changed at"), auto_now=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("User Image")
        verbose_name_plural = _("User Images")

    def __str__(self) -> str:
        return self.user.get_username()
