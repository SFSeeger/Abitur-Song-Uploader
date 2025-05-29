from crispy_bulma.widgets import FileUploadInput
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pictures.models import PictureField
from tinymce import models as tinymce_models

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
    answers = GenericRelation("polls.answer")

    def get_template(self):
        raise NotImplementedError("Method 'get_template' needs to be subclassed")

    class Meta:
        abstract = True


class CharAnswerValue(AnswerValue):
    value = models.CharField(_("Value"), max_length=512)

    def get_template(self):
        return "polls/answervalue/char.html"


def generate_poll_filename(self, filename):
    return "images/%s" % (filename)


class ImageAnswerValue(AnswerValue):
    width = models.IntegerField()
    height = models.IntegerField()
    value = PictureField(
        _("Image"),
        upload_to=generate_poll_filename,
        aspect_ratios=[None, "1/1"],
        width_field="width",
        height_field="height",
    )

    def get_template(self):
        return "polls/answervalue/image.html"


class MultipleChoiceAnswerValue(AnswerValue):
    value = models.ManyToManyField("polls.Option", verbose_name=_("Values"))

    def get_template(self):
        return "polls/answervalue/multiple.html"


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
        widgets = {"value": FileUploadInput}


class MULTIPLE_CHOICE_ANSWER_FORM(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        self.question = kwargs.pop("question")
        self.max_answers = self.question.max_answers
        self.choices = self.question.option_set.all()

        super().__init__(*args, **kwargs)

        widget = None
        if self.choices.count() > 15:
            widget = slim_select.MultipleSlimSelect(max_answers=self.max_answers)
        else:
            widget = forms.widgets.CheckboxSelectMultiple

        self.fields["value"] = forms.ModelMultipleChoiceField(
            widget=widget,
            queryset=self.choices,
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
    description = tinymce_models.HTMLField(_("Description"))
    start_date = models.DateTimeField(_("Start Date"), auto_now_add=True)
    end_date = models.DateField(_("End Date"))
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
    description = tinymce_models.HTMLField(_("Description"))
    max_answers = models.PositiveSmallIntegerField(
        _("Max Answers"),
        help_text=_("Max amounts of Answers that can be given"),
        default=1,
        blank=True,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    poll = models.ForeignKey(
        "polls.Poll", verbose_name=_("Poll"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_form(self):
        return self.FORM_OPTIONS[self.question_type]

    def get_absolute_url(self):
        return reverse("question-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["position", "created_at", "name"]


class Response(models.Model):
    poll = models.ForeignKey(
        "polls.Poll", verbose_name=_("Poll"), on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "auth.User", verbose_name=_("User"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poll} - {self.user}"

    class Meta:
        ordering = ["created_at"]


class Answer(models.Model):
    question = models.ForeignKey(
        "polls.Question", verbose_name=_("Question"), on_delete=models.CASCADE
    )
    response = models.ForeignKey(
        "polls.Response", verbose_name=_("Response"), on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    answer_value = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

@receiver(post_delete, sender=Answer)
def delete_answer_value(sender, instance, **kwargs):
    print(instance, "deleted")
    if instance.answer_value:
        instance.answer_value.delete()