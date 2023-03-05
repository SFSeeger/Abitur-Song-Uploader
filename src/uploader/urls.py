from django.urls import path
from .views import LoginView, LogoutView, IndexView, SubmissionCreateView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("upload/", SubmissionCreateView.as_view(), name="upload"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
