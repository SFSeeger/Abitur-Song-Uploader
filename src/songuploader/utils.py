import os
import shutil
from datetime import datetime
from typing import Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from yt_dlp import YoutubeDL

from songuploader.settings import MEDIA_ROOT
from uploader.models import Submission


class ConfiguredLoginViewMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"


class LoginRequiredTemplateView(ConfiguredLoginViewMixin, TemplateView):
    template_name: str = None


class UnderConstructionView(View):
    def get(self, request, *args, **kwargs):
        message = '<span class="icon-text"><span class="icon"><i class="fa-solid fa-wrench"></i></span><span>%s</span></span>'
        messages.info(
            request,
            mark_safe(
                message % _("The side you tried to access is under construction")
            ),
        )
        return redirect("index")


class DisabledOnDateMixin:
    end_date: datetime
    date_redirect_url: str
    message_content: Optional[str] = None

    def dispatch(self, request, *args, **kwargs):
        if timezone.now() >= self.end_date:
            if self.message_content:
                messages.info(request, self.message_content)
            return redirect(self.date_redirect_url)
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"


def download_song(submission: Submission):
    mp4_out_path = os.path.join(settings.MEDIA_ROOT, "tmp", f"{submission.user.id}.mp4")
    mp3_out_path = os.path.join(settings.MEDIA_ROOT, "tmp", f"{submission.user.id}.mp3")
    ydl_opts = {
        "outtmpl": mp4_out_path,
        "format": "bestaudio/best",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([submission.song_url])
    os.system(f"ffmpeg -i {mp4_out_path} -y -vn {mp3_out_path}")
    open_file = open(mp3_out_path, "rb")
    song_file: File = File(open_file)
    submission.song = song_file
    submission.save()
    os.remove(mp4_out_path)
    os.remove(mp3_out_path)


def download_song_url(song_url: str, filename: str) -> str:
    mp4_out_path = os.path.join(settings.MEDIA_ROOT, "tmp", f"{filename}.mp4")
    mp3_out_path = os.path.join(settings.MEDIA_ROOT, "tmp", f"{filename}.mp3")
    ydl_opts = {
        "outtmpl": mp4_out_path,
        "format": "bestaudio/best",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_url])
    os.system(f"ffmpeg -i {mp4_out_path} -y -vn {mp3_out_path}")
    os.remove(mp4_out_path)
    return mp3_out_path


def slice_song(submission: Submission):
    out_path = os.path.join(
        settings.MEDIA_ROOT, "tmp", os.path.basename(submission.song.name)
    )
    shutil.copy2(submission.song.path, out_path)
    os.system(
        f"ffmpeg -ss {submission.start_time} -i {out_path} -c copy -y -t {submission.end_time-submission.start_time} {submission.song.path}"
    )
    os.remove(out_path)


def slice_song_path(filepath: str, start_time: str, end_time: str) -> str:
    filename, extension = os.path.splitext(os.path.basename(filepath))
    input_path = os.path.join(
        settings.MEDIA_ROOT, "tmp", filename + f"_full{extension}"
    )
    os.system(
        f"ffmpeg -ss {start_time} -i {input_path} -c copy -y -t {end_time-start_time} {filepath}"
    )
    return filepath


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
