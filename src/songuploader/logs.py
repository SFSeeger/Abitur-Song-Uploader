import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver
from django.utils import timezone

log = logging.getLogger(__name__)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    # to cover more complex cases:
    # http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    ip = request.META.get("REMOTE_ADDR")
    log.debug(f"{ip} - {user} Login")


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR")
    log.debug(f"{ip} - {user} Logout")


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    ip = request.META.get("REMOTE_ADDR")
    log.warning(f"{ip} Login failed")
