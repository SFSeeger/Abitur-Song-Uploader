import logging
import os

from .base import *

ADMINS = [("ADMIN", ADMIN_EMAIL)]

STATIC_ROOT = os.environ.get("STATIC_ROOT", "/var/www/data/static")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", "/var/www/data/media")

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
DEFAULT_FROM_EMAIL = f"{os.environ.get('EMAIL_SENDER', 'Abitur Song Uploader')} <{os.environ.get('EMAIL_HOST_USER')}>"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False").lower() == "true"

PROMETHEUS_METRICS_EXPORT_PORT_RANGE = range(9200, 9204)
PROMETHEUS_METRICS_EXPORT_ADDRESS = ""
PROMETHEUS_EXPORT_MIGRATIONS = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app": {
            "format": (
                "%(asctime)s [%(levelname)-8s] " "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.environ.get("DJANGO_LOG_FILE", "/var/log/django/error.log"),
            "formatter": "app",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
        "django": {
            "handlers": ["file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}
