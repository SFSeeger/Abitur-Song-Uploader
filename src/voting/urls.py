from django.urls import path
from .views import CreateFormView, SubmitVoteFormView

urlpatterns = [
    path("vote", SubmitVoteFormView.as_view()),
    path("option", CreateFormView.as_view())
]