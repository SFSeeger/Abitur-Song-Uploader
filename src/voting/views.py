import json
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from songuploader.utils import (
    ConfiguredLoginViewMixin,
    DisabledOnDateMixin,
    LoginRequiredTemplateView,
)

from .forms import VoteForm
from .models import Option, Vote


class VoteFormView(ConfiguredLoginViewMixin, DisabledOnDateMixin, FormView):
    template_name = "voting/vote.html"
    form_class = VoteForm
    success_url = reverse_lazy("vote-dashboard")

    end_date = timezone.make_aware(
        timezone.datetime(2023, 3, 23, 23, 59), timezone.get_default_timezone()
    )
    date_redirect_url = "vote-dashboard"

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
