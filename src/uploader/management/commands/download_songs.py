from django.core.management.base import BaseCommand
from django_q.tasks import async_chain, async_task

from songuploader.utils import download_song, slice_song
from uploader.models import Submission
from uploader.views.submission_views import download_slice


class Command(BaseCommand):
    help = "To manually redownload/slice songs for users"

    def handle(self, *args, **options):
        for submission in Submission.objects.filter(song=None):
            if submission.song_url:
                async_chain([(download_song, [submission]), (slice_song, [submission])])
