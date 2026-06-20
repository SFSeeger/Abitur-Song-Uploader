from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def get_public_domain(request):
    return {
        "domain": get_current_site(request),
        "protocol": "https" if request.is_secure() or not request else "http",
    }


def get_settings_context(request):
    return {
        "ADMIN_EMAIL": settings.ADMIN_EMAIL,
        "CURRENT_YEAR": settings.CURRENT_YEAR,
        "SCHOOL_NAME": settings.SCHOOL_NAME,
    }
