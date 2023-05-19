import logging
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
from songuploader.utils import ConfiguredLoginViewMixin, get_client_ip

from ..forms import LoginForm
from ..models import Submission

log = logging.getLogger("django")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "uploader/login_view.html"

    def form_valid(self, form) -> HttpResponse:
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        ip = get_client_ip(self.request)

        if user is not None:
            login(self.request, user)
            log.info(f'"{ip} - {user} Login"')

            redirect_to = form.cleaned_data.get("redirect_to")
            return redirect(redirect_to if redirect_to else "/")
        else:
            log.warning(f'"{ip} - {form.cleaned_data["username"]} Login failed"')
            messages.error(self.request, _("Wrong username or password"))
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        log.info(f'"{get_client_ip(self.request)} - {self.request.user} Logout"')
        logout(request)
        return redirect("login")


class IndexView(ConfiguredLoginViewMixin, TemplateView):
    template_name = "uploader/index.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["has_song"] = Submission.objects.filter(user=self.request.user).first()
        context["polls"] = get_user_polls(self.request.user)
        return context
