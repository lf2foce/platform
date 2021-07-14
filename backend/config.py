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

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
SECRET_KEY = config('SECRET_KEY', cast=Secret)


# database
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret)

# this will support special chars for credentials
_DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
_QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
DATABASE_NAME = config("DATABASE_NAME", default="loki")
DATABASE_PORT = config("DATABASE_PORT", default="3306")
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{_DATABASE_CREDENTIAL_USER}:{_QUOTED_DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

#đang test
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default='redis://127.0.0.1:6379')
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default='redis://127.0.0.1:6379')
CELERY_ACCEPT_CONTENT = config("CELERY_ACCEPT_CONTENT", default=['application/json'])
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
