from os import environ, path, pardir

from api.constants import (
    DEFAULT_LOGGER_LEVEL,
    DEFAULT_DB_PASSWORD,
    DEFAULT_DB_CLUSTER,
    DEFAULT_DB_USER,
    DEFAULT_DB_NAME,
    DEFAULT_DB_HOST,
)

SERVICE_NAME = environ.get("SERVICE_NAME", "partner-api")
LOGGER_NAME = environ.get("LOGGER_NAME", SERVICE_NAME)
LOGGER_LEVEL = environ.get("LOGGER_LEVEL", DEFAULT_LOGGER_LEVEL)
DB_NAME = environ.get("DB_NAME", DEFAULT_DB_NAME)
DB_USER = environ.get("DB_USER", DEFAULT_DB_USER)
DB_CLUSTER = environ.get("DB_CLUSTER", DEFAULT_DB_CLUSTER)
DB_HOST = environ.get("DB_HOST", DEFAULT_DB_HOST)
DB_PASSWORD = environ.get("DB_PASSWORD", DEFAULT_DB_PASSWORD)
VERSION = environ.get("VERSION", "0.1.0")
APP_ENV = environ.get("APP_ENV", "local").upper()
PORT = environ.get("PORT", "3000")
HOST = environ.get("HOST", "0.0.0.0")
SERVICE_ROOT = path.abspath(path.dirname(__file__))
PROJECT_ROOT = path.abspath(path.join(SERVICE_ROOT, pardir))
