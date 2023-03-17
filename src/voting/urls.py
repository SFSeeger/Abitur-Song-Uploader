from django.urls import path
from .views import SubmitVoteFormView

urlpatterns = [
    path("vote", SubmitVoteFormView.as_view()),
]
