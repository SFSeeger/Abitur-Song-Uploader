from crispy_bulma.forms import FileField
from crispy_bulma.layout import Field, Layout, Submit, UploadField
from crispy_bulma.widgets import FileUploadInput
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Hidden, Row
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Profile, UserImage


class UserImageForm(forms.ModelForm):
    image = FileField()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            UploadField("image", css_class="input"),
        )
        self.helper.add_input(
            Submit("submit", _("Submit"), css_class="is-primary is-fullwidth")
        )

    class Meta:
        model = UserImage
        fields = ["image"]


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            
        )
        self.helper.add_input(
            Submit("submit", _("Submit"), css_class="is-primary is-fullwidth")
        )

    class Meta:
        model = Profile
        exclude = ["user"]
