import pathlib
from pathlib import Path

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from songuploader.utils import download_song_url, slice_song_path
from uploader.models import Submission
import shutil
import os
from songuploader.settings import MEDIA_ROOT

User = get_user_model()

TMP_DIR = pathlib.Path(os.path.join(MEDIA_ROOT, "tmp"))
PLAYLIST_DIR = TMP_DIR.joinpath("playlist")

class Command(BaseCommand):
    help = "Creates a playlist containing all songs ordered by lastname then by firstname"

    def add_arguments(self, parser):
        parser.add_argument(
            "-e",
            "--exclude",
            nargs="+",
            default=[],
            help="Excludes users from the playlist",
            metavar="USERNAME",
        )

        default_song_group = parser.add_mutually_exclusive_group(required=True)
        default_song_group.add_argument(
            "-y",
            "--youtube",
            type=str,
            default=None,
            help="YouTube URL for the default song for users without a submission",
            nargs=3,
            metavar=("URL", "START_TIME", "END_TIME")
        )

        default_song_group.add_argument(
            "-s",
            "--song",
            type=Path,
            default=None,
            help="Song path for the default song for users without a submission",
        )

    def handle(self, *args, **options):
        users = User.objects.order_by('last_name', 'first_name')
        exclude = options["exclude"]

        default_song_path = options["song"]
        PLAYLIST_DIR.mkdir(parents=True, exist_ok=True)

        if options["youtube"]:
            url, start_time, end_time = options["youtube"]
            start_time = int(start_time)
            end_time = int(end_time)
            song_path = download_song_url(url, "default_song")
            default_song_path = slice_song_path(song_path, start_time, end_time)

        for i, user in enumerate(users):
            # Skip excluded users
            if user.username in exclude:
                continue

            user_submission = Submission.objects.filter(user=user).first()
            if user_submission and user_submission.song:
                song_path = user_submission.song.path
            else:
                song_path = default_song_path
            _, extension =  os.path.splitext(song_path)
            shutil.copy2(song_path, PLAYLIST_DIR.joinpath(f"{i}_{user.last_name}_{user.first_name}{extension}"))
        shutil.make_archive(os.path.join(MEDIA_ROOT, "playlist"), "zip", PLAYLIST_DIR)
        shutil.rmtree(TMP_DIR)