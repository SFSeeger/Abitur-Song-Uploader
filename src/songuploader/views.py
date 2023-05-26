import logging
from typing import Any

from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponse

from .utils import get_client_ip

log = logging.getLogger("django")


class LoggingPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    html_email_template_name = "users/email/password_reset_email.html"

    def form_valid(self, form: Any) -> HttpResponse:
        email = form.cleaned_data["email"]
        ip = get_client_ip(self.request)
        
        log.info(f'"{ip} - {email} Password Reset"')
        return super().form_valid(form)
