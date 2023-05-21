from crispy_bulma.layout import Column, Row, Submit
from crispy_bulma.widgets import FileUploadInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

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
                _("Update Poll") if self.initial else _("Create Poll"),
                css_class="is-primary is-fullwidth is-rounded",
            ),
        )

    class Meta:
        model = Poll
        fields = ["name", "end_date", "description", "can_answered_multiple"]

        widgets = {
            "end_date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }


class CSVOptionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "file",
            Submit(
                "submit",
                _("Submit"),
                css_class="is-primary is-fullwidth is-rounded",
            ),
        )

    file = forms.FileField(
        label=_("File"),
        validators=[FileExtensionValidator(["csv"])],
        widget=FileUploadInput,
    )
