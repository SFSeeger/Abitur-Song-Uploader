# Create your models here.
import os
from typing import Any, Dict, Mapping, Optional, Type, Union

from crispy_bulma.layout import Submit
from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from django.db import models
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pictures.models import PictureField

from theme.utils import generate_filename
from theme.widgets import slim_select


class Option(models.Model):
    name = models.CharField(_("Name"), max_length=64)
    question = models.ForeignKey(
        "polls.Question", verbose_name=_("Question"), on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Option")
        verbose_name_plural = _("Options")


class AnswerValue(models.Model):
    answer = GenericRelation("polls.answer", object_id_field="answer_value_id")

    class Meta:
        abstract = True


class CharAnswerValue(AnswerValue):
    value = models.CharField(_("Value"), max_length=512)


def generate_poll_filename(self, filename):
    return "images/%s" % (filename)


class ImageAnswerValue(AnswerValue):
    width = models.IntegerField()
    height = models.IntegerField()
    value = PictureField(
        _("Image"),
        upload_to=generate_poll_filename,
        aspect_ratios=[None, "1/1", "3/4"],
        width_field="width",
        height_field="height",
    )


class MultipleChoiceAnswerValue(AnswerValue):
    value = models.ManyToManyField("polls.Option", verbose_name=_("Values"))


class CHAR_ANSWER_FORM(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop("question")
        super().__init__(*args, **kwargs)

    class Meta:
        model = CharAnswerValue
        fields = ["value"]


class IMAGE_ANSWER_FORM(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop("question")
        super().__init__(*args, **kwargs)

    class Meta:
        model = ImageAnswerValue
        fields = ["value"]


class MULTIPLE_CHOICE_ANSWER_FORM(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        self.question = kwargs.pop("question")
        self.max_answers = self.question.max_answers
        self.choices = self.question.option_set.all()

        super().__init__(*args, **kwargs)

        if self.choices.count() > 15:
            self.fields["value"].widget = slim_select.MultipleSlimSelect(
                choices=self.choices
            )
        else:
            self.fields["value"].widget = forms.widgets.CheckboxSelectMultiple(
                choices=self.choices
            )

    def clean_value(self):
        data = self.cleaned_data["value"]
        if data.count() > self.max_answers:
            raise forms.ValidationError(
                _("Only %(max_answers)s options possible"),
                code="invalid",
                params={"max_answers": self.max_answers},
            )
        return data

    class Meta:
        model = MultipleChoiceAnswerValue
        fields = ["value"]


class Poll(models.Model):
    name = models.CharField(_("Name"), max_length=64)
    description = models.CharField(_("Description"), max_length=512)
    start_date = models.DateTimeField(_("Start Date"), auto_now_add=True)
    end_date = models.DateTimeField(_("End Date"))
    can_answered_multiple = models.BooleanField(_("Can be answered multiple times"))

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("question-filter", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
        permissions = [
            ("can_open_polls", _("Can open Polls")),
            ("can_close_polls", _("Can close Polls")),
        ]
        ordering = ["-end_date"]


class Question(models.Model):
    TYPE_CHOICES = (
        (0, _("Text Type")),
        (1, _("Image Type")),
        (2, _("Multiple Choice Type")),
    )
    FORM_OPTIONS = [CHAR_ANSWER_FORM, IMAGE_ANSWER_FORM, MULTIPLE_CHOICE_ANSWER_FORM]

    question_type = models.IntegerField(_("Question Type"), choices=TYPE_CHOICES)
    position = models.PositiveIntegerField(
        _("Position"), help_text=_("Order in which questions are displayed"), default=0
    )

    name = models.CharField(_("Name"), max_length=64)
    description = models.CharField(_("Description"), max_length=512)
    max_answers = models.PositiveSmallIntegerField(
        _("Max Answers"),
        help_text=_("Max amounts of Answers that can be given"),
        default=1,
        blank=True,
    )

    poll = models.ForeignKey(
        "polls.Poll", verbose_name=_("Poll"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_form(self):
        return self.FORM_OPTIONS[self.question_type]

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["position"]


class Response(models.Model):
    poll = models.ForeignKey(
        "polls.Poll", verbose_name=_("Poll"), on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "auth.User", verbose_name=_("User"), on_delete=models.CASCADE
    )


class Answer(models.Model):
    question = models.ForeignKey(
        "polls.Question", verbose_name=_("Question"), on_delete=models.CASCADE
    )
    response = models.ForeignKey(
        "polls.Response", verbose_name=_("Response"), on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    answer_value_id = models.PositiveIntegerField()
    answer_value = GenericForeignKey("content_type", "answer_value_id")