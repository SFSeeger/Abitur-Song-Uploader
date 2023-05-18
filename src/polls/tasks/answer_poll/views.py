from typing import Any, Dict, Type

from django import forms, http
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from polls.models import CHAR_ANSWER_FORM, Answer, Poll, Question, Response
from polls.utils import get_question
from songuploader.utils import ConfiguredLoginViewMixin


class StartPollView(ConfiguredLoginViewMixin, SingleObjectMixin, TemplateView):
    model = Poll
    template_name = "polls/answer_poll/start_poll.html"
    object = None

    def post(self, request, *args, **kwargs):
        response, idx = self.get_response()
        if not response:
            return redirect("index")

        return redirect("question-answer", pk=response.id, question_idx=idx)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

    def get_response(self):
        response = Response.objects.filter(user=self.request.user, poll=self.object)
        if response.exists():
            response = response.last()
            poll = response.poll
            # Check if Poll is already answered
            if response.answer_set.count() == poll.question_set.count():
                if not poll.can_answered_multiple:
                    messages.error(
                        self.request, _("You have already answered this poll")
                    )
                    return (None, None)
                return (self.create_poll(), 0)
            return (response, response.answer_set.count())
        return (self.create_poll(), 0)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        if self.object.end_date < timezone.now().date():
            messages.warning(request, _("Poll is closed"))
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def create_poll(self):
        response = Response(user=self.request.user, poll=self.object)
        response.save()
        return response


class QuestionAnswerView(ConfiguredLoginViewMixin, SingleObjectMixin, FormView):
    model = Response
    template_name = "polls/answer_poll/question_answer_form.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not get_question(self.poll, self.kwargs.get("question_idx")):
            return redirect("poll-done")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: Any) -> HttpResponse:
        answer_value = form.save()
        Answer.objects.create(
            question=self.question, response=self.object, answer_value=answer_value
        )
        return redirect(
            "question-answer",
            pk=self.object.id,
            question_idx=self.kwargs.get("question_idx") + 1,
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(FormView, self).get_context_data(**kwargs)
        context["poll"] = self.poll
        context["question"] = self.question
        return context

    def get_form_class(self) -> type:
        if self.question:
            return self.question.get_form()
        return CHAR_ANSWER_FORM

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), question=self.question)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        self.poll = self.object.poll
        self.question = get_question(self.poll, self.kwargs.get("question_idx"))
        if not self.object.user == request.user:
            raise PermissionDenied()
        if self.object.answer_set.filter(question=self.question).exists():
            raise PermissionDenied()
        if self.poll.end_date < timezone.now().date():
            messages.warning(request, _("Poll is closed"))
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)
