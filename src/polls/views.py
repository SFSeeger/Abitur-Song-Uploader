from typing import Any, Dict, Optional

from django import http
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, TemplateView, UpdateView
from django_filters.views import FilterView

from polls.filters import PollFilter, QuestionFilter
from polls.forms import QuestionForm, ResponseFilterForm
from polls.models import Option, Poll, Question
from polls.tasks.create_poll.forms import PollForm
from theme.widgets.slim_select import MultipleSlimSelect


class PollFilterView(PermissionRequiredMixin, FilterView):
    permission_required = "polls.can_open_polls"
    filterset_class = PollFilter

    def get_paginate_by(self, queryset) -> Optional[int]:
        return self.request.GET.get("page_size", 10)


class PollUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "polls.can_open_polls"
    model = Poll
    form_class = PollForm


class PollDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "polls.can_open_polls"
    model = Poll

    def get_success_url(self) -> str:
        return reverse("poll-filter")


class QuestionFilterView(PermissionRequiredMixin, FilterView):
    permission_required = "polls.can_open_polls"
    filterset_class = QuestionFilter

    def get_paginate_by(self, queryset) -> Optional[int]:
        return self.request.GET.get("page_size", 10)

    def get_queryset(self):
        self.poll = get_object_or_404(Poll, id=self.kwargs.get("pk"))
        return Question.objects.filter(poll=self.poll)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["poll"] = self.poll
        return context


class QuestionDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "polls.can_open_polls"
    model = Question

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class QuestionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "polls.can_open_polls"
    model = Question
    form_class = QuestionForm

    def get_success_url(self) -> str:
        return reverse("question-detail", kwargs={"pk": self.get_object().id})


class QuestionDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "polls.can_open_polls"
    model = Question

    def get_success_url(self) -> str:
        return self.get_object().poll.get_absolute_url()


class OptionDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "polls.can_open_polls"
    model = Option

    def get_success_url(self) -> str:
        return reverse("question-detail", kwargs={"pk": self.get_object().question.id})


User = get_user_model()
slimselect = MultipleSlimSelect(
    attrs={"id": "id_user_id"},
    choices=((x.id, f"{x.first_name} {x.last_name}") for x in User.objects.all()),
).render("user_id", "user_id")


class AnswerDetailView(PermissionRequiredMixin, TemplateView):
    permission_required = "polls.can_open_polls"
    template_name = "polls/answer_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        poll = get_object_or_404(Poll, pk=self.kwargs.get("pk"))
        context["object"] = poll
        responses = poll.response_set.filter(
            user__in=self.request.GET.getlist("user_id")
        )
        context["responses"] = responses
        context["slimselect"] = slimselect
        return context
