from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from crispy_bulma.layout import Submit, Field


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
