from django.core.management.base import BaseCommand
from uploader.models import Submission
from uploader.views.submission_views import download_slice
from django_q.tasks import async_task
from songuploader.utils import slice_song, download_song
from django_q.tasks import async_chain

class Command(BaseCommand):
    help = "To manually redownload/slice songs for users"

    def handle(self, *args, **options):
        for submission in Submission.objects.filter(song=''):
            if submission.song_url:
                async_chain([(download_song, [submission]), (slice_song, [submission])])
            else:
                async_task(slice_song, submission)
