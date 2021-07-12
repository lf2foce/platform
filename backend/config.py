import logging
import os
import base64
from urllib import parse
from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.datastructures import Secret

log = logging.getLogger(__name__)

config = Config(".env")

# static files
DEFAULT_STATIC_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "static/loki"
)
STATIC_DIR = config("STATIC_DIR", default=DEFAULT_STATIC_DIR)


# database
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret)

# this will support special chars for credentials
_DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
_QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
DATABASE_NAME = config("DATABASE_NAME", default="loki")
DATABASE_PORT = config("DATABASE_PORT", default="3306")
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{_DATABASE_CREDENTIAL_USER}:{_QUOTED_DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
