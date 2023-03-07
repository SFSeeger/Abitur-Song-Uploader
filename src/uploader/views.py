from typing import Any
import requests
import re
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, CreateView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import LoginForm, SubmissionForm
from .models import Submission


class LoginView(FormView):
    form_class = LoginForm
    template_name = "uploader/login_view.html"

    def form_valid(self, form) -> HttpResponse:
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(self.request, user)
            redirect_to = form.cleaned_data.get("redirect_to")
            return redirect(redirect_to if redirect_to else "/")
        else:
            messages.error(self.request, _("Wrong username or password"))
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"

    template_name = "uploader/test.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["lang_code"] = self.request.LANGUAGE_CODE
        return context


class SubmissionCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"

    model = Submission
    form_class = SubmissionForm
    template_name = "uploader/upload_form.html"
    redirect_url = reverse_lazy("index")

    pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
    yt_url = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"

    def try_site(self, url):
        request = requests.get(url)
        return False if self.pattern in request.text else True

    def form_valid(self, form):
        if not re.match(self.yt_url, form.cleaned_data["song_url"]):
            return super().form_invalid()
        if not self.try_site(form.cleaned_data["song_url"]):
            return super().form_invalid()

        submission = form.save(commit=False)
        submission.user = self.request.user
        submission.save()
        return HttpResponseRedirect(self.redirect_url)
