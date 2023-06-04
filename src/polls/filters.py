from django import forms
from django.contrib.auth import get_user_model
from django.db.models import DateField, Q
from django.utils.translation import gettext_lazy as _
from django_filters import (
    BooleanFilter,
    CharFilter,
    DateTimeFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
)

from polls.models import Poll, Question, Response
from theme.widgets.slim_select import MultipleSlimSelect


class PollFilter(FilterSet):
    search = CharFilter(
        field_name="search", method="search_filter", widget=forms.HiddenInput
    )

    def search_filter(self, queryset, name, value):
        values = [v.strip() for v in value.split(" ")]
        for v in values:
            if not value:
                continue
            queryset = queryset.filter(
                Q(name__icontains=value) | Q(description__icontains=value)
            )
        return queryset

    class Meta:
        model = Poll
        fields = ["end_date"]

        filter_overrides = {
            DateField: {
                "filter_class": DateTimeFilter,
                "extra": lambda f: {
                    "widget": forms.DateInput(attrs={"type": "date"}),
                },
            },
        }


class QuestionFilter(FilterSet):
    search = CharFilter(
        field_name="search", method="search_filter", widget=forms.HiddenInput
    )

    def search_filter(self, queryset, name, value):
        values = [v.strip() for v in value.split(" ")]
        for v in values:
            if not value:
                continue
            queryset = queryset.filter(
                Q(name__icontains=value) | Q(description__icontains=value)
            )
        return queryset

    class Meta:
        model = Question
        fields = [
            "question_type",
        ]


User = get_user_model()


# class ResponseFilter(FilterSet):
#     show_empty_responses = BooleanFilter(
#         choices=((False, _("No")), (True, _("Yes"))), method="show_empty_filter"
#     )
#     users = forms.ModelMultipleChoiceFilter(
#         User.objects.all(), widget=MultipleSlimSelect()
#     )

#     class Meta:
#         model = Response
#         fields = [
#             "user",
#         ]

#     def show_empty_filter(self, queryset, name, value):
#         if value == "False":
#             queryset.exclude()
