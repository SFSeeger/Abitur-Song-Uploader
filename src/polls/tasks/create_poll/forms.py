from crispy_bulma.layout import Column, Row, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Button, Field, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from polls.models import Option, Poll, Question


class PollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("name"), Column("end_date")),
            "description",
            "can_answered_multiple",
            Submit(
                "submit",
                _("Create Poll"),
                css_class="is-primary is-fullwidth is-rounded",
            ),
        )

    class Meta:
        model = Poll
        fields = ["name", "end_date", "description", "can_answered_multiple"]

        widgets = {
            "description": forms.widgets.Textarea(attrs={"rows": 2}),
            "end_date": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
        }
