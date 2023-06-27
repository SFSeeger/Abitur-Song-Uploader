import logging
import os
import shutil
from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.files import File
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView

from polls.utils import get_user_polls
from songuploader.settings import MEDIA_ROOT, MEDIA_URL
from songuploader.utils import (
    ConfiguredLoginViewMixin,
    download_song_url,
    get_client_ip,
    slice_song_path,
)

from ..forms import LoginForm, PlaylistDownloadForm
from ..models import Submission

log = logging.getLogger("django")

User = get_user_model()


class LoginView(FormView):
    form_class = LoginForm
    template_name = "uploader/login_view.html"

    def form_valid(self, form) -> HttpResponse:
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        ip = get_client_ip(self.request)

        if user is not None:
            login(self.request, user)
            log.info(f'"{ip} - {user} Login"')

            redirect_to = form.cleaned_data.get("redirect_to")
            return redirect(redirect_to if redirect_to else "/")
        else:
            log.warning(f'"{ip} - {form.cleaned_data["username"]} Login failed"')
            messages.error(self.request, _("Wrong username or password"))
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        log.info(f'"{get_client_ip(self.request)} - {self.request.user} Logout"')
        logout(request)
        return redirect("login")


class IndexView(ConfiguredLoginViewMixin, TemplateView):
    template_name = "uploader/index.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["has_song"] = Submission.objects.filter(user=self.request.user).first()
        context["polls"] = get_user_polls(self.request.user)
        return context


class DownloadPlaylistView(FormView):
    template_name = "uploader/playlist.html"
    form_class = PlaylistDownloadForm

    def form_valid(self, form):
        if not os.path.exists(os.path.join(MEDIA_ROOT, "tmp", "playlist")):
            os.mkdir(os.path.join(MEDIA_ROOT, "tmp", "playlist"))
        if not (song := form.files["song"]):
            filename = os.path.basename(
                download_song_url(form.cleaned_data["song_url"])
            )
            file = open(slice_song_path(filename))
            song = File(file)
        users = User.objects.order_by("last_name", "first_name").prefetch_related(
            "submission_set"
        )
        for i, user in enumerate(users):
            if not user.submission_set.first():
                default_storage.save(
                    os.path.join("tmp/playlist", f"{i}_{user}.mp3"), song
                )
            else:
                song_path = user.submission_set.first().song.path
                shutil.copy2(
                    song_path,
                    os.path.join(
                        os.path.join(MEDIA_ROOT, "tmp", "playlist"), f"{i}_{user}.mp3"
                    ),
                )
        shutil.make_archive(
            os.path.join(MEDIA_ROOT, "playlist"),
            "zip",
            os.path.join(MEDIA_ROOT, "tmp", "playlist"),
        )
        return redirect(MEDIA_URL + "tmp/playlist.zip")
