from django import forms
from django.db.models import DateField, Q
from django_filters import CharFilter, DateTimeFilter, FilterSet

from polls.models import Poll, Question


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
