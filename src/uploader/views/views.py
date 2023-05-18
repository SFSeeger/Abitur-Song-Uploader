from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView

from polls.utils import get_user_polls
from songuploader.utils import ConfiguredLoginViewMixin

from ..forms import LoginForm
from ..models import Submission


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


class IndexView(ConfiguredLoginViewMixin, TemplateView):
    template_name = "uploader/index.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["has_song"] = Submission.objects.filter(user=self.request.user).first()
        context["polls"] = get_user_polls(self.request.user)
        return context
