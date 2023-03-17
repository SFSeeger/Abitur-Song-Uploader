from django.urls import path
from .views import SubmitVoteFormView
from django.views.generic import TemplateView

urlpatterns = [
    path("vote", SubmitVoteFormView.as_view()),
]
