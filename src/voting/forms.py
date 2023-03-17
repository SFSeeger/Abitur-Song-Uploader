from django import forms
from .models import Option

from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_bulma.layout import Submit


class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        self.helper = FormHelper()
        super().__init__(*args, **kwargs)
        self.helper.add_input(
            Submit(
                "submit", _("Submit"), css_class="is-primary is-fullwidth is-rounded"
            )
        )

    options = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Option.objects.all()
    )

    def clean_options(self):
        data = self.cleaned_data["options"]
        if data.count() > 5:
            raise forms.ValidationError(
                _("Only 5 options possible"),
                code="invalid",
            )
        return data
