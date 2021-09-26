import traceback
from datetime import datetime
from json import dumps
from logging import getLogger, Handler, StreamHandler, Logger as BaseLogger
from sys import stdout

from api.constants import (
    LOG_LEVEL_CRITICAL,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_INFO,
    LOG_LEVEL_DEBUG,
)
from api.vars import LOGGER_NAME, LOGGER_LEVEL


class Logger:
    _name: str = None
    __logger: BaseLogger = None

    @classmethod
    def start_logger(
        cls, log_level: str = None, log_name: str = None, handler: Handler = None
    ) -> BaseLogger:
        getLogger("multipart.multipart").disabled = True

        cls._name = log_name if log_name else LOGGER_NAME
        cls.__logger = getLogger(cls._name)
        logger_handler = handler if handler else StreamHandler(stream=stdout)
        cls.__logger.addHandler(logger_handler)
        cls.__logger.setLevel(log_level if log_level else LOGGER_LEVEL)

        return cls.__logger

    @classmethod
    def _do_log(cls, level: str, message: str, **kwargs: dict) -> None:
        level = level.upper()
        level_selector = {
            LOG_LEVEL_CRITICAL: cls.__logger.fatal,
            LOG_LEVEL_ERROR: cls.__logger.error,
            LOG_LEVEL_WARNING: cls.__logger.warning,
            LOG_LEVEL_INFO: cls.__logger.info,
            LOG_LEVEL_DEBUG: cls.__logger.debug,
        }
        log_json = cls._format_message_attributes(message=message, level=level, **kwargs)
        log = level_selector.get(level, LOG_LEVEL_INFO)
        log(msg=log_json)

    @classmethod
    def critical(cls, message: str, **kwargs: dict) -> None:
        cls._do_log(level=LOG_LEVEL_CRITICAL, message=message, **kwargs)

    @classmethod
    def error(cls, message: str, **kwargs) -> None:
        cls._do_log(level=LOG_LEVEL_ERROR, message=message, **kwargs)

    @classmethod
    def warning(cls, message: str, **kwargs: dict) -> None:
        cls._do_log(level=LOG_LEVEL_WARNING, message=message, **kwargs)

    @classmethod
    def info(cls, message: str, **kwargs: dict) -> None:
        cls._do_log(level=LOG_LEVEL_INFO, message=message, **kwargs)

    @classmethod
    def debug(cls, message: str, **kwargs: dict) -> None:
        cls._do_log(level=LOG_LEVEL_DEBUG, message=message, **kwargs)

    @staticmethod
    def _format_traceback():
        trace = traceback.format_exc()
        if not trace:
            return None

        trace = trace.splitlines()
        traceback_dict = {"traceback": trace[1:]}

        for i in range(0, len(traceback_dict["traceback"])):
            traceback_dict["traceback"][i] = (
                traceback_dict["traceback"][i].replace('"', "").strip()
            )

        return traceback_dict

    @staticmethod
    def _format_message_attributes(message: str, level: str, **kwargs: dict) -> str:

        record = dict()
        record["severity"] = level
        record["message"] = message
        record["message_data"] = kwargs
        record["timestamp"] = str(datetime.utcnow())
        trace = Logger._format_traceback()
        if trace:
            record["traceback"] = trace
        return dumps(record, sort_keys=True)
