from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_bulma.layout import Submit, Field
from crispy_bulma.widgets import FileUploadInput

from .models import Submission


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Field("username", autocomplete="off"),
            Field(
                "username",
                autocomplete="off",
                template="bulma/layout/input_with_icon.html",
                icon_prepend="fa-solid fa-user",
            ),
            Field("password"),
            # Submit("submit", _("Submit")),
        )
        self.helper.add_input(
            Submit("submit", _("Submit"), css_class="is-primary is-fullwidth")
        )

    username = forms.CharField(max_length=512, required=True, label=_("Username"))
    password = forms.CharField(
        max_length=512, required=True, widget=forms.PasswordInput(), label=_("Password")
    )


class SubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("song_url", "start_time", "song")
        self.helper.add_input(
            Submit("submit", _("Submit"), css_class="is-primary is-fullwidth")
        )

    class Meta:
        model = Submission
        fields = ["song_url", "start_time", "song"]
        widgets = {"song": FileUploadInput()}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("song_url") and cleaned_data.get("song"):
            raise ValidationError(_("You can't set song url and song at the same time"))
