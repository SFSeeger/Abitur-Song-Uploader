from .base import *

ALLOWED_HOSTS = [os.environ.get("WEBSITE_URL")]
ADMINS = [("ADMIN", ADMIN_EMAIL)]

STATIC_ROOT = "/var/www/data/static"
STATIC_URL = "/static/"
MEDIA_ROOT = "/var/www/data/media"

EMAIL_HOST = "smtp.gmail.com"
DEFAULT_FROM_EMAIL = f"RG Abi 2023 <{os.environ.get('EMAIL_HOST_USER')}>"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

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
            "filename": "/var/log/django/error.log",
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}
