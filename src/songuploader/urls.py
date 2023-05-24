from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from songuploader.utils import UnderConstructionView

urlpatterns = [
    path("", include("uploader.urls")),
    path("vote/", include("voting.urls")),
    path("poll/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("construction/", UnderConstructionView.as_view(), name="under-construction"),
    path("tinymce/", include("tinymce.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
