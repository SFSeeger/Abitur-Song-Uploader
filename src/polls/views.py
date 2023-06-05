import time
from typing import Any, Dict, Optional

from django import http
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    DeleteView,
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
)
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterView

from polls.filters import PollFilter, QuestionFilter
from polls.forms import QuestionForm
from polls.models import CHAR_ANSWER_FORM, Answer, Option, Poll, Question, Response
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
        question = self.get_object()
        if question.question_type == 2:
            context["data"] = list(
                Option.objects.filter(question=question)
                .annotate(count=Count("multiplechoiceanswervalue"))
                .filter(count__gt=0)
                .order_by("-count")
                .values("name", "count")
            )
            # context["data"] = {item["name"]: item["count"] for item in values}
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


class UserResponseView(TemplateView):
    template_name = "polls/user_answer_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["responses"] = Response.objects.filter(user=self.request.user)
        return context


class ResponseDeleteView(DeleteView):
    model = Response

    def get_success_url(self) -> str:
        return reverse("answer-detail", kwargs={"pk": self.get_object().poll})

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if not (
            self.get_object().user == request.user
            or request.user.has_perm("polls.can_open_polls")
            or request.user.is_superuser
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AnswerEditView(SingleObjectMixin, FormView):
    model = Answer
    template_name = "polls/answer_form.html"
    object = None

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        answer_value = form.save()
        answer = self.get_object()
        answer.answer_value = answer_value
        answer.save()
        if (
            self.request.user.has_perm("polls.can_open_polls")
            or self.request.user.is_superuser
        ):
            return redirect("answer-detail", kwargs={"pk": answer.response.poll.id})
        return redirect("user-response-detail")

    def get_initial(self) -> Dict[str, Any]:
        value = self.get_object().answer_value.value
        return {"value": value.all() if self.question.question_type == 2 else value}

    def get_form_class(self) -> type:
        if self.question:
            return self.question.get_form()
        return CHAR_ANSWER_FORM

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), question=self.question)

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        self.question = self.get_object().question
        if not (
            self.get_object().response.user == request.user
            or request.user.has_perm("polls.can_open_polls")
            or request.user.is_superuser
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["question"] = self.question
        return context


class AnswerDeleteView(DeleteView):
    model = Answer

    def get_success_url(self) -> str:
        if (
            self.request.user.has_perm("polls.can_open_polls")
            or self.request.user.is_superuser
        ):
            return reverse(
                "answer-detail", kwargs={"pk": self.get_object().response.poll.id}
            )
        return reverse("user-response-detail")

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if not (
            self.get_object().response.user == request.user
            or request.user.has_perm("polls.can_open_polls")
            or request.user.is_superuser
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
