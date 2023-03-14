from django.urls import path, include

from songuploader.utils import LoginRequiredTemplateView
from .forms import SubmissionUploadForm
from .views.submission_views import SubmissionCreateView, SubmissionUpdateView
from .views.file_views import FileDownload
from .views.views import (
    LoginView,
    LogoutView,
    IndexView,
)

song_urlpatterns = [
    path(
        "choose/",
        LoginRequiredTemplateView.as_view(
            template_name="uploader/choose_upload_type.html"
        ),
        name="choose-song",
    ),
    path("from-youtube/", SubmissionCreateView.as_view(), name="from-youtube"),
    path(
        "from-youtube/update/<int:pk>",
        SubmissionUpdateView.as_view(),
        name="update-from-youtube",
    ),
    path(
        "from-file/",
        SubmissionCreateView.as_view(
            form_class=SubmissionUploadForm, update_name="update-from-file"
        ),
        name="from-file",
    ),
    path(
        "from-file/update/<int:pk>",
        SubmissionUpdateView.as_view(form_class=SubmissionUploadForm),
        name="update-from-file",
    ),
    path("upload/", SubmissionCreateView.as_view(), name="upload"),
]

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("song/", include(song_urlpatterns)),
    path("file/<str:filename>/", FileDownload.as_view(), name="download-file"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
