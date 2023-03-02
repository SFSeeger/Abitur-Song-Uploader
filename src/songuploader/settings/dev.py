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
print("AAA")
