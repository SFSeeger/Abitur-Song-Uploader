from typing import Any
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from songuploader.utils import ConfiguredLoginViewMixin, LoginRequiredTemplateView
from .forms import VoteForm
from .models import Vote, Option
import json


class VoteFormView(ConfiguredLoginViewMixin, FormView):
    template_name = "voting/vote.html"
    form_class = VoteForm
    success_url = reverse_lazy("vote-dashboard")

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if Vote.objects.filter(user=self.request.user):
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: VoteForm):
        # Check if user has already submitted
        user_votes = Vote.objects.filter(user=self.request.user)
        if user_votes.exists():
            return redirect(self.success_url)

        # else create Vote
        vote = Vote.objects.create(user=self.request.user)
        vote.options.set(form.cleaned_data["options"])
        vote.save()
        return super().form_valid(form)


class DashboardView(LoginRequiredTemplateView):
    template_name = "voting/dashboard.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data()
        response_data = {}
        for option in Option.objects.all():
            response_data[option.name] = option.vote_set.count()
        response_data = dict(
            sorted(response_data.items(), key=lambda item: item[1])[::-1]
        )
        context["chart"] = mark_safe(json.dumps(response_data))
        context["data"] = response_data
        context["votes"] = Vote.objects.all().count()

        return context
