from typing import Any, Dict, Optional

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django_filters.views import FilterView

from polls.filters import PollFilter, QuestionFilter
from polls.forms import QuestionForm
from polls.models import Option, Poll, Question
from polls.tasks.create_poll.forms import PollForm


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
