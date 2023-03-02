import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

if os.environ.get("ENVIRONMENT") == "dev":
    from .dev import *
