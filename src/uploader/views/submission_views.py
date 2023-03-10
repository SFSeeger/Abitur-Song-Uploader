from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from songuploader.utils import ConfiguredLoginViewMixin

from ..forms import SubmissionForm
from ..models import Submission


class SubmissionCreateView(ConfiguredLoginViewMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "uploader/upload_form.html"
    success_url = reverse_lazy("index")
    update_name = "update-from-youtube"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if obj := Submission.objects.filter(user=self.request.user):
            return redirect(reverse(self.update_name, kwargs={"pk": obj.first().pk}))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if Submission.objects.filter(user=self.request.user).exists():
            return HttpResponse(status=412)
        Submission.objects.create(**form.cleaned_data, user=self.request.user)
        return HttpResponseRedirect(self.success_url)


class SubmissionUpdateView(ConfiguredLoginViewMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "uploader/upload_form.html"
    success_url = reverse_lazy("index")
