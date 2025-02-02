import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, DateField, Exists, F, OuterRef, Q, Subquery, Value
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_filters import (
    BooleanFilter,
    CharFilter,
    DateTimeFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
)

from polls.models import Answer, AnswerValue, CharAnswerValue, Poll, Question, Response
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


class ResponseFilter(FilterSet):
    user = ModelMultipleChoiceFilter(
        field_name="user", queryset=User.objects.all(), widget=MultipleSlimSelect
    )

    def get_answer_value_class(
        self, queryset, question_name: str
    ) -> (list[Answer], AnswerValue):
        answers = Answer.objects.filter(
            response__in=queryset, question__name=question_name
        )
        AnswerValue = None
        if answers.exists():
            AnswerValue = answers.first().content_type.model_class()
        return answers, AnswerValue

    def filter_text(self, queryset, name, value):
        if not value:
            return queryset
        values = [v.strip() for v in value.split(" ")]
        query = Q()
        for v in values:
            query.add(Q(value__icontains=v), Q.OR)

        answers, AnswerValue = self.get_answer_value_class(queryset, name)

        answer_values = AnswerValue.objects.filter(query).values_list("id", flat=True)
        filtered_answers = answers.filter(answer_value_id__in=answer_values)
        return queryset.filter(answer__in=filtered_answers).distinct()

    def filter_many_to_many(self, queryset, name, value):
        if not value:
            return queryset
        answers, AnswerValue = self.get_answer_value_class(queryset, name)

        answer_values = AnswerValue.objects.filter(value__in=value).values_list(
            "id", flat=True
        )
        filtered_answers = answers.filter(answer_value_id__in=answer_values)
        return queryset.filter(answer__in=filtered_answers).distinct()

    def get_filter(self, question: Question):
        name = question.name
        if question.question_type == 0:
            return CharFilter(field_name=name, method=self.filter_text, label=name)
        if question.question_type == 2:
            return ModelMultipleChoiceFilter(
                method=self.filter_many_to_many,
                field_name=name,
                queryset=question.option_set.all(),
                widget=MultipleSlimSelect,
                label=name,
            )

    def __init__(self, *args, **kwargs):
        poll: Poll = kwargs.pop("poll")
        super().__init__(*args, queryset=poll.response_set.all(), **kwargs)
        questions: list[Question] = poll.question_set.all()
        for question in questions:
            if question.question_type == 1:
                continue
            self.filters[re.sub("[^0-9a-zA-Z_]+", "_", question.name.lower())] = (
                self.get_filter(question)
            )

    class Meta:
        model = Response
        fields = ["user"]
