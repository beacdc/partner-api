from logging import Logger as BaseLogger

from pytest import fixture

from api.logging.logger import Logger
from api.vars import LOGGER_NAME, LOGGER_LEVEL, SERVICE_NAME


@fixture(scope="class")
def logger() -> BaseLogger:
    Logger.start_logger()
    return Logger


def test_config_get_default_logger_name():
    assert LOGGER_NAME == SERVICE_NAME


def test_config_get_default_logger_level():
    assert LOGGER_LEVEL == "DEBUG"


def test_create_logger_return_logger():
    logger = Logger.start_logger()
    assert type(logger) is BaseLogger


def test_logger_has_default_logger_name(logger):
    assert LOGGER_NAME == logger._name
