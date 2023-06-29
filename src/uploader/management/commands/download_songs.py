from django.core.management.base import BaseCommand
from django_q.tasks import async_chain, async_task

from songuploader.utils import download_song, slice_song
from uploader.models import Submission
from uploader.views.submission_views import download_slice


class Command(BaseCommand):
    help = "To manually redownload/slice songs for users"

    def handle(self, *args, **options):
        submissions = Submission.objects.filter(song="")
        for idx, submission in enumerate(submissions):
            self.stdout.write(
                f"Processing submission {idx}{submissions.count()}: {submission}\n"
            )
            if submission.song_url:
                download_song(submission)
                slice_song(submission)
