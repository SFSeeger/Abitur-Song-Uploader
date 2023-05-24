from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from songuploader.utils import UnderConstructionView

account_patterns = [
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            html_email_template_name="users/email/password_reset_email.html",
        ),
        name="password-reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

urlpatterns = [
    path("", include("uploader.urls")),
    path("vote/", include("voting.urls")),
    path("poll/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include(account_patterns)),
    path("construction/", UnderConstructionView.as_view(), name="under-construction"),
    path("tinymce/", include("tinymce.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
