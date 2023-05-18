from django.urls import include, path

import polls.tasks.answer_poll.urls as answer_urls
import polls.tasks.create_poll.urls as create_urls
import polls.views as views

urlpatterns = [
    path("", views.PollFilterView.as_view(), name="poll-filter"),
    path("<int:pk>/edit", views.PollUpdateView.as_view(), name="poll-update"),
    path("<int:pk>/delete", views.PollDeleteView.as_view(), name="poll-delete"),
    path("", include(create_urls)),
    path("", include(answer_urls)),
    path("<int:pk>/", views.QuestionFilterView.as_view(), name="question-filter"),
    path(
        "question/<int:pk>/", views.QuestionDetailView.as_view(), name="question-detail"
    ),
    path(
        "question/edit/<int:pk>/",
        views.QuestionUpdateView.as_view(),
        name="question-update",
    ),
    path(
        "question/<int:pk>/delete/",
        views.QuestionDeleteView.as_view(),
        name="question-delete",
    ),
    path(
        "option/<int:pk>/delete/",
        views.OptionDeleteView.as_view(),
        name="option-delete",
    ),
]
