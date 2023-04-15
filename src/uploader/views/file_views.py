from pathlib import Path
from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404, HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
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
