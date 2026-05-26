import os
import logging
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv(raise_error_if_not_found=False))

if os.environ.get("ENVIRONMENT") == "dev":
    from .dev import *
    logger.info("Loading development settings")
else:
    from .prod import *
    logger.info("Loading production settings")
