from django.urls import include, path

from songuploader.utils import LoginRequiredTemplateView

from .views import QuestionAnswerView, StartPollView

urlpatterns = [
    path("start/<int:pk>/", StartPollView.as_view(), name="poll-start"),
    path(
        "question/<int:pk>/<int:question_idx>",
        QuestionAnswerView.as_view(),
        name="question-answer",
    ),
    path(
        "done/",
        LoginRequiredTemplateView.as_view(
            template_name="polls/answer_poll/poll_done.html"
        ),
        name="poll-done",
    ),
]
