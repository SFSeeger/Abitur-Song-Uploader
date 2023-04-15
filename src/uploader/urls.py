from django.urls import include, path, re_path
from django.views.generic.base import TemplateView

from songuploader.utils import LoginRequiredTemplateView, slice_song

from .forms import SubmissionUploadForm
from .views.file_views import FileDownload
from .views.submission_views import SubmissionCreateView, SubmissionUpdateView
from .views.views import IndexView, LoginView, LogoutView

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
            form_class=SubmissionUploadForm,
            update_name="update-from-file",
            submit_action=slice_song,
        ),
        name="from-file",
    ),
    path(
        "from-file/update/<int:pk>",
        SubmissionUpdateView.as_view(
            form_class=SubmissionUploadForm, submit_action=slice_song
        ),
        name="update-from-file",
    ),
    path("upload/", SubmissionCreateView.as_view(), name="upload"),
]


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("song/", include(song_urlpatterns)),
    re_path(r"^media/(?P<path>.*)/$", FileDownload.as_view(), name="download-file"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
