from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from songuploader.utils import ConfiguredLoginViewMixin
from .forms import VoteForm
from .models import Vote, Option
import json


class SubmitVoteFormView(ConfiguredLoginViewMixin, FormView):
    template_name = "voting/vote.html"
    form_class = VoteForm
    success_url = "/"

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

class ShowDashboardView(TemplateView):
    template_name = "voting/dashboard.html"

    def get_context_data(self, **kwargs: Any):
        response_data = {}
        for option in Option.objects.all():
            response_data[option.name] = option.vote_set.count()
        return {'chart': json.dumps(response_data)}
