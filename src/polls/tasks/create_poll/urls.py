from django.urls import include, path

from .views import (
    CSVOptionCreateView,
    OptionCreateView,
    PollCreateView,
    QuestionCreateView,
)

urlpatterns = [
    path("create/", PollCreateView.as_view(), name="poll-create"),
    path(
        "option/create/<int:question_id>",
        OptionCreateView.as_view(),
        name="question-option-create",
    ),
    path(
        "option/create/csv/<int:pk>",
        CSVOptionCreateView.as_view(),
        name="question-option-csv-create",
    ),
    path(
        "question/create/<int:poll_id>",
        QuestionCreateView.as_view(),
        name="question-create",
    ),
]
