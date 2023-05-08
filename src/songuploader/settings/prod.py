from .base import *

ALLOWED_HOSTS = ["sfseeger.ddns.net", "intern.rgabi.de"]
ADMINS = [("Simon", "simon.f.seeger@gmx.de")]

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

PROMETHEUS_METRICS_EXPORT_PORT_RANGE = range(8001, 8020)
PROMETHEUS_METRICS_EXPORT_ADDRESS = ""
PROMETHEUS_EXPORT_MIGRATIONS = False
