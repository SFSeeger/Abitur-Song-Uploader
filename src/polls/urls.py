from django.urls import include, path

import polls.tasks.create_poll.urls as create_urls
import polls.views as views

urlpatterns = [
    path("", views.PollFilterView.as_view(), name="poll-filter"),
    path("", include(create_urls)),
    path("<int:pk>/", views.QuestionFilterView.as_view(), name="question-filter"),
    path(
        "question/<int:pk>/", views.QuestionDetailView.as_view(), name="question-detail"
    ),
    path(
        "question/edit/<int:pk>/",
        views.QuestionUpdateView.as_view(),
        name="question-update",
    ),
]
