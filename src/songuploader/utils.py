from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View


class ConfiguredLoginViewMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")
    redirect_field_name = "redirect_to"


class LoginRequiredTemplateView(ConfiguredLoginViewMixin, TemplateView):
    template_name: str = None
