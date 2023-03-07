from django.urls import path, include

from songuploader.utils import LoginRequiredTemplateView
from .views import (
    LoginView,
    LogoutView,
    IndexView,
    SubmissionCreateView,
    SubmissionUpdateView,
)

song_urlpatterns = [
    path(
        "choose/",
        LoginRequiredTemplateView.as_view(template_name="uploader/choose_song.html"),
        name="choose-song",
    ),
    path("from-youtube/", SubmissionCreateView.as_view(), name="from-youtube"),
    path(
        "from-youtube/update/<int:pk>",
        SubmissionUpdateView.as_view(),
        name="update-from-youtube",
    ),
    path("upload/", SubmissionCreateView.as_view(), name="upload"),
]

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("song/", include(song_urlpatterns)),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
