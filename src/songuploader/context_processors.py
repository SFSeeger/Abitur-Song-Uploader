from django.conf import settings


def get_public_domain(request):
    return {"public_domain": settings.PUBLIC_DOMAIN}
