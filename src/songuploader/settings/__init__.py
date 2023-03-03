import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))

if os.environ.get("ENVIRONMENT") == "dev":
    from .dev import *
else:
    from .base import *
