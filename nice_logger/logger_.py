from __future__ import annotations
import sys

import loguru
from loguru import logger

from nice_logger.logger_assets import print_tbl, format_extra_obj
from nice_logger.config import config

# https://flaviocopes.com/rgb-color-codes/
# https://loguru.readthedocs.io/en/stable/api/logger.html#message
# https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.complete
# https://docs.python.org/3/library/string.html#format-string-syntax
# https://loguru.readthedocs.io/en/stable/resources/recipes.html#adapting-colors-and-format-of-logged-messages-dynamically
# https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.level
# https://encycolorpedia.ru/30d5c8 - colors

"""
    TRACE	    5	nice_logger.trace()
    DEBUG	    10	nice_logger.debug()
    INFO	    20	nice_logger.info()
    SUCCESS	    25	nice_logger.success()
    WARNING	    30	nice_logger.warning()
    ERROR	    40	nice_logger.error()
    CRITICAL	50	nice_logger.critical()
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


def format_regular_record(record: loguru.Record) -> str:
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
                sys.stdout.write("\033[F")  # back to previous line
                # sys.stdout.write("\033[K")  # clear line
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
log = logger.opt(lazy=False, colors=True).bind(name="all")
