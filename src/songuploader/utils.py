import os
from datetime import datetime
from typing import Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from pytube import YouTube

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


def download_song(url: str, submission: Submission):
    out_path = os.path.join("/tmp", f"{submission.user.username}_temp.wav")
    YouTube(url=url).streams.filter(only_audio=True).first().download(
        output_path=os.path.dirname(out_path), filename=os.path.basename(out_path)
    )
    open_file = open(out_path, "rb")
    song_file: File = File(open_file)
    submission.song = song_file
    submission.save()
    os.remove(out_path)
