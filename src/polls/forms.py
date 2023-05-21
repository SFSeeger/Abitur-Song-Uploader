from crispy_bulma.layout import Column, Row, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Button, Field, Layout
from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from polls.models import Option, Poll, Question


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column(Field("name")), Column(Field("position"))),
            Row(
                Column(Field("question_type")),
                Column("max_answers"),
            ),
            "description",
            Submit(
                "submit",
                _("Update Question") if self.initial else _("Create Question"),
                css_class="is-primary is-fullwidth is-rounded",
            ),
        )
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["question_type"].disabled = True

    class Meta:
        model = Question
        fields = [
            "name",
            "position",
            "question_type",
            "description",
            "max_answers",
        ]

    def clean_max_answers(self):
        data = self.cleaned_data.get("max_answers", 1)
        data = 1 if data == None else data
        choice = self.cleaned_data["question_type"]
        if choice != 2 and data > 1:
            raise forms.ValidationError(
                _("Max Answers has to be one on this question type")
            )

        return data

    def clean_question_type(self):
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            return instance.question_type
        else:
            return self.cleaned_data.get("question_type", None)


class BaseOptionFormset(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseOptionFormset, self).__init__(*args, **kwargs)
        self.queryset = Option.objects.none()
