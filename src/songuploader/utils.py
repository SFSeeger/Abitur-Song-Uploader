from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from pytube import YouTube
from settings import MEDIA_ROOT
from django.core.files import File
from uploader.models import Submission
from django.contrib.auth.models import AbstractBaseUser
import os 


class LoginRequiredTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"

    template_name: str = None

def download_song(name: str, url: str, **kwargs):
    YouTube(url=url).streams.first().download(output_path=MEDIA_ROOT, filename=name)
    open_file = open(MEDIA_ROOT / name, 'r')
    song_file: File = File(open_file)
    new_submission = Submission(user=kwargs['user'], song_url=url, start_time=kwargs['start_time'], end_time=kwargs['end_time'], song=song_file)
    new_submission.save()

def slice_song(user):
    submission = Submission.objects.filter(user__id=user)
    if not submission:
        return
    os.system(f'cp {submission.song.path} /tmp/{os.path.basename(submission.song.name)}')
    os.system(f'ffmpeg -ss {submission.start_time} -i /tmp/{os.path.basename(submission.song.name)} -c copy -t {submission.end_time-submission.start_time} {submission.song.path} -y') # Pray this works simon or elese you gonna hear a lot bout dynamically tiped languages !
    os.system(f'rm /tmp/{os.path.basename(submission.song.name)}')