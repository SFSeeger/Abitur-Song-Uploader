from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from pytube import YouTube
from songuploader.settings import MEDIA_ROOT
from django.core.files import File
from uploader.models import Submission
import os


class ConfiguredLoginViewMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"


class LoginRequiredTemplateView(ConfiguredLoginViewMixin, TemplateView):
    template_name: str = None


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
