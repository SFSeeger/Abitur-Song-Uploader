from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import LoginView, LogoutView, IndexView, SubmissionCreateView
from songuploader.utils import LoginRequiredTemplateView

songpatterns = [
    path(
        "",
        LoginRequiredTemplateView.as_view(
            template_name="uploader/choose_upload_type.html"
        ),
        name="choose-upload",
    ),
    path("from-youtube/", SubmissionCreateView.as_view(), name="from-youtube"),
    path("upload/", SubmissionCreateView.as_view(), name="song-upload"),
]

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("song/", include(songpatterns), name="choose-upload"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
