from typing import Any, Dict, Optional

import pandas as pd
from django import http
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models, transaction
from django.forms import BaseModelForm, modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormView

from polls.filters import PollFilter
from polls.forms import BaseOptionFormset, QuestionForm
from polls.models import Option, Poll, Question

from .forms import CSVOptionForm, PollForm


class PollCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "polls.can_open_polls"
    model = Poll
    form_class = PollForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse("question-create", kwargs={"poll_id": self.object.id})


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
        Option, fields=("name",), formset=BaseOptionFormset
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
            return HttpResponseRedirect(
                reverse("question-detail", kwargs={"pk": question.id})
            )
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if not "formset" in kwargs:
            context["formset"] = self.formset_class()
        return context


class CSVOptionCreateView(PermissionRequiredMixin, FormView):
    permission_required = "polls.can_open_polls"
    form_class = CSVOptionForm
    model = Question
    template_name = "polls/csv_option_form.html"
    object = None

    def get_object(self):
        if not self.object:
            return get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        return self.object

    def form_valid(self, form: CSVOptionForm) -> HttpResponse:
        csv = form.files["file"]
        df = pd.read_csv(csv, delimiter=";")
        with transaction.atomic():
            for idx, row in df.iterrows():
                Option.objects.create(question=self.get_object(), name=row["name"])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()
