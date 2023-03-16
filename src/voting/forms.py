from django import forms
from .models import Option

class CreateForm(forms.Form):
    name = forms.CharField(max_length=200)

class VoteForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Option.objects.all())