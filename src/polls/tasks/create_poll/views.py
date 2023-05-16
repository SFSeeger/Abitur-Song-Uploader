from typing import Any, Dict

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.forms import BaseModelForm, modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView

from polls.filters import PollFilter
from polls.forms import QuestionForm
from polls.models import Option, Poll, Question
from songuploader.utils import LoginRequiredTemplateView

from .forms import PollForm


class PollCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "polls.can_open_polls"
    model = Poll
    form_class = PollForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse("question-create", kwargs={"question_id": self.object.id})


class QuestionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "polls.can_open_polls"
    model = Question
    form_class = QuestionForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        question: Question = form.save(commit=False)
        question.poll = get_object_or_404(Poll, id=self.kwargs.get("poll_id"))
        question.save()
        return HttpResponseRedirect(
            reverse(
                "question-detail",
                kwargs={"pk": question.id},
            )
        )


class OptionCreateView(PermissionRequiredMixin, TemplateView):
    permission_required = "polls.can_open_polls"
    formset_class = modelformset_factory(
        Option, fields=("name",), extra=1, can_delete=True
    )
    template_name = "polls/option_form.html"

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, id=self.kwargs["question_id"])

        formset = self.formset_class(request.POST)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    if form.is_valid():
                        option = form.save(commit=False)
                        option.question = question
                        option.save()
            return HttpResponseRedirect(reverse("question-detail", question.id))
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if not "formset" in kwargs:
            context["formset"] = self.formset_class()
        return context
