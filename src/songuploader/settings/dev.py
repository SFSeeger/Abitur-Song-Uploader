from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "db",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": "3306",
    }
}

MEDIA_ROOT = "media/"
FILE_UPLOAD_PERMISSIONS = 0o644

EMAIL_HOST = "mailhog"
DEFAULT_FROM_EMAIL = "RG Abi Song <sfseeger.ddns.net>"
EMAIL_PORT = 1025
