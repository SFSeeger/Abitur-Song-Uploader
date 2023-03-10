import requests
import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Hidden, Row, Div
from crispy_forms.bootstrap import PrependedText
from crispy_bulma.layout import Submit, Field, Layout, UploadField
from crispy_bulma.forms import FileField

from .models import Submission


pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
yt_url = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


def try_site(video_id: str) -> bool:
    request = requests.get(f"http://img.youtube.com/vi/{video_id}/mqdefault.jpg")
    return request.status_code == 200


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            PrependedText(
                "username",
                "fa-solid fa-user",
                css_class="input",
                autocomplete="off",
            ),
            PrependedText(
                "password",
                "fa-solid fa-lock",
                css_class="input",
            ),
            Hidden("redirect_to", value="", id="redirect_to"),
        )
        self.helper.add_input(
            Submit(
                "submit", _("Submit"), css_class="is-primary is-fullwidth is-rounded"
            )
        )

    username = forms.CharField(max_length=512, required=True, label=_("Username"))
    password = forms.CharField(
        max_length=512, required=True, widget=forms.PasswordInput(), label=_("Password")
    )
    redirect_to = forms.CharField(max_length=512, required=False)


class SubmissionBaseForm(forms.ModelForm):
    def clean_end_time(self):
        start_time = self.cleaned_data["start_time"]
        end_time = self.cleaned_data["end_time"]

        if start_time > end_time:
            raise ValidationError(
                _("Start Time cannot be larger than End Time"), code="invalid"
            )
        elif (duration := (end_time - start_time)) > 30:
            raise ValidationError(
                _("Duration of %(duration)d larger than 30 seconds"),
                code="invalid",
                params={"duration": duration},
            )
        return end_time


class SubmissionForm(SubmissionBaseForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            PrependedText("song_url", "fa-brands fa-youtube", css_class="input"),
            Row(
                Div("start_time", css_class="column"),
                Div("end_time", css_class="column"),
            ),
        )
        self.helper.add_input(
            Submit("submit", _("Submit"), css_class="is-primary is-fullwidth")
        )

    class Meta:
        model = Submission
        fields = ["song_url", "start_time", "end_time"]

    def clean_song_url(self):
        data = self.cleaned_data["song_url"]

        if not (match := re.match(yt_url, data)):
            raise ValidationError(
                _("Not a valid YouTube url: %(value)s"),
                code="invalid",
                params={"value": data},
            )
        elif not try_site(match[6]):
            raise ValidationError(
                _("Could not find YouTube video"),
                code="invalid",
            )

        return data


class SubmissionUploadForm(SubmissionBaseForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            UploadField("song", css_class="input"),
            Row(
                Div("start_time", css_class="column"),
                Div("end_time", css_class="column"),
            ),
        )
        self.helper.add_input(
            Submit("submit", _("Submit"), css_class="is-primary is-fullwidth")
        )

    song = FileField(required=True)

    class Meta:
        model = Submission
        fields = ["song", "start_time", "end_time"]
