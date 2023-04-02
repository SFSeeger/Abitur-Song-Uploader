from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from django_q.tasks import async_chain, async_task

from songuploader.utils import ConfiguredLoginViewMixin, download_song, slice_song

from ..forms import SubmissionForm
from ..models import Submission


def download_slice(view, submission: Submission):
    async_chain(
        [
            (download_song, [submission]),
            (slice_song, [submission]),
        ]
    )


def slice_anon(view, submission: Submission):
    slice_song(submission)


class SubmissionCreateView(ConfiguredLoginViewMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "uploader/upload_form.html"
    success_url = reverse_lazy("index")
    update_name = "update-from-youtube"
    submit_action = download_slice

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if obj := Submission.objects.filter(user=self.request.user):
            return redirect(reverse(self.update_name, kwargs={"pk": obj.first().pk}))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if Submission.objects.filter(user=self.request.user).exists():
            return HttpResponse(status=412)
        submission = Submission.objects.create(
            **form.cleaned_data, user=self.request.user
        )
        # async_task(self.submit_action, submission)
        self.submit_action(submission)
        return HttpResponseRedirect(self.success_url)


class SubmissionUpdateView(ConfiguredLoginViewMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "uploader/upload_form.html"
    success_url = reverse_lazy("index")
    submit_action = download_slice

    def form_valid(self, form):
        submission = form.save()

        # async_task(self.submit_action, submission)
        self.submit_action(submission)
        return HttpResponseRedirect(self.success_url)
