from __future__ import annotations
import sys
import loguru
from loguru import logger

from logger.logger_assets import print_tbl, format_extra_obj
from logger.config import config

# https://flaviocopes.com/rgb-color-codes/
# https://loguru.readthedocs.io/en/stable/api/logger.html#message
# https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.complete
# https://docs.python.org/3/library/string.html#format-string-syntax
# https://loguru.readthedocs.io/en/stable/resources/recipes.html#adapting-colors-and-format-of-logged-messages-dynamically
# https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.level
# https://encycolorpedia.ru/30d5c8 - colors

"""
    TRACE	    5	logger.trace()
    DEBUG	    10	logger.debug()
    INFO	    20	logger.info()
    SUCCESS	    25	logger.success()
    WARNING	    30	logger.warning()
    ERROR	    40	logger.error()
    CRITICAL	50	logger.critical()
"""


logger.remove()


def format_exception_record(record: loguru.Record) -> str:
    """форматирует записи исключений"""
    message = record["message"]
    line = record["line"]
    level = record["level"]
    file = record["file"]
    msg = print_tbl(level=level, message=message, file=file, line=line, style="error")
    record["extra"]["msg"] = msg
    return config.LOGURU_EXCEPTION_FORMAT_LONG


def format_regular_record(record: loguru.Record) -> dict:
    """форматирует все записи кроме исключений"""
    message = record["message"]
    line = record["line"]
    level = record["level"]
    file = record["file"]
    extra = record.get("extra")
    LOGURU_GENERIC_FORMAT = "{extra[msg]}"
    if level:
        msg = print_tbl(
            level=level, message=message, file=file, line=line, style=level.name.lower()
        )
        if extra:
            obj = extra.get("o")
            record["extra"]["msg"] = msg
            if obj:
                record["extra"]["obj"] = format_extra_obj(obj)
                return LOGURU_GENERIC_FORMAT + "\n{extra[obj]}"
    return LOGURU_GENERIC_FORMAT


# для всех записей кроме исключений
logger.add(
    sink=sys.stdout,
    level=config.LOG_LEVEL,
    format=format_regular_record,
    backtrace=False,
    catch=False,
    filter=lambda record: record["extra"].get("name") == "all",
)


# только для исключений
# сначала работает synk, затем форматтер
logger.add(
    sink=sys.stderr,
    filter=lambda record: record["extra"].get("name") == "err",
    format=format_exception_record,
    backtrace=False,
    catch=True,
)


errlog = logger.opt(colors=True, exception=True).bind(name="err")
log_ = logger.opt(colors=True).bind(name="all")


def print_log(level: str, *args, **kwargs) -> None:
    """Helper for print records"""
    if isinstance(args[0], dict):
        return getattr(log_, level)("", o=args[0])
    obj = kwargs.get("o")

    if obj:
        return getattr(log_, level)(args[0], o=obj)

    return getattr(log_, level)(args[0])


class Logger:
    """Обёртка над loguru"""

    @staticmethod
    def debug(*args, **kwargs) -> None:
        print_log("debug", *args, **kwargs)

    @staticmethod
    def trace(*args, **kwargs) -> None:
        print_log("trace", *args, **kwargs)

    @staticmethod
    def info(*args, **kwargs) -> None:
        print_log("info", *args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs) -> None:
        print_log("warning", *args, **kwargs)

    @staticmethod
    def success(*args, **kwargs) -> None:
        print_log("success", *args, **kwargs)

    @staticmethod
    def error(*args, **kwargs) -> None:
        print_log("error", *args, **kwargs)

    @staticmethod
    def critical(*args, **kwargs) -> None:
        print_log("critical", *args, **kwargs)


log = Logger()
