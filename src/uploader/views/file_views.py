from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.views.generic import View

from songuploader.utils import ConfiguredLoginViewMixin


class FileDownload(ConfiguredLoginViewMixin, View):
    def get(self, request, *args, **kwargs):
        file = Path(settings.MEDIA_ROOT).joinpath(kwargs.get("path")).absolute()
        try:
            f = open(file, "rb")
            return FileResponse(f)
        except (FileNotFoundError, IsADirectoryError):
            raise Http404
