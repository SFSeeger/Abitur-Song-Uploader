from django.urls import path
from .views import VoteFormView, DashboardView
from django.views.generic import TemplateView

urlpatterns = [
    path("vote/", VoteFormView.as_view(), name="add-vote"),
    path("dashboard/", DashboardView.as_view(), name="vote-dashboard"),
]
