from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from uploader.models import Submission
import shutil
import os
from songuploader.settings import MEDIA_ROOT

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.order_by('lastname', 'firstname').values()
        for i, user in enumerate(users):
            user_submission = Submission.objects.filter(user=user)
            if not user_submission:
                # Default song
                pass 
            song_path = user_submission.first().song.path
            shutil.copy2(song_path, os.path.join(os.path.join(MEDIA_ROOT, "playlist"), f"{i}.{os.path.splittext(song_path)}"))
        shutil.make_archive(os.path.join(MEDIA_ROOT, "playlist"), "zip", os.path.join(MEDIA_ROOT, "playlist"))