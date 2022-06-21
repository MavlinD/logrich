import sys
from typing import NamedTuple

from loguru import logger, _handler
from rich import json
from rich.errors import MissingStyle, MarkupError
from rich.pretty import pprint
from rich.table import Table

from logger.logger_assets import print_tbl, console, console_dict, print_tbl_obj, ccapt
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


class FirstLine(NamedTuple):
    """первая строка лога"""

    level: str
    message: str
    # source: str
    file: str
    line: str


class MySynk:
    max_len = config.MAX_WITH_LOG_OF_OBJ
    compilied_message = None
    is_printed_compile_message = False
    is_compile_error = None

    def __init__(self, log_entry: _handler.Message):
        """печатает запись лога"""
        self.log_entry = log_entry

        # https://rich.readthedocs.io/en/stable/_modules/rich/highlighter.html
        # https://rich.readthedocs.io/en/stable/highlighting.html
        # https://loguru.readthedocs.io/en/stable/resources/recipes.html#serializing-log-messages-using-a-custom-function

        self.level = self.log_entry.record["level"].name.lower()
        self.obj = self.log_entry.record.get("extra").get("o")
        print_rule = self.log_entry.record.get("extra").get("rule")
        self._message = self.log_entry.record["message"]
        self.restore_message()
        # self.print_log_header()
        self.print_compiled_message()
        self.print_obj()
        if print_rule:
            console.rule(style="#33adff")

    def print_log_header(self) -> None:
        """печатает строку уровня - заголовок лога"""
        first = self.log_entry.replace("%level%", f"[{self.level}]").replace("\n", "")
        parts = first.split("%%")
        # return
        self.print_first(
            FirstLine(
                level=parts[0],
                message=self.message,
                file=parts[1],
                line=parts[2],
                # source=parts[1]
            )
        )

    @property
    def message(self) -> str:
        if len(self._message) < self.max_len:
            return self._message
        if self.compilied_message:
            return ""
        return self._message

    def print_first(self, first_line: FirstLine):
        """печать сообщения"""
        style = f"{self.level}"
        # style = f"{self.level}_msg"
        try:

            msg = print_tbl(
                level=first_line.level,
                message=first_line.message,
                file=first_line.file,
                line=first_line.line,
                style=style,
            )
            console_dict.print(msg)

        except MissingStyle:
            pprint(f"Стиль {style} не найден")
        except MarkupError as err:
            pprint(err)
            ...

    def restore_message(self):
        """пытается сериализовать основное тело записи лога"""
        if not self.obj:
            if len(self._message) >= self.max_len:
                try:
                    # self.compilied_message = eval(self._message)
                    ...
                except SyntaxError as err:
                    # pprint(err)
                    self.is_compile_error = True
                    # вероятно это строка
                    ...
                except NameError as err:
                    # pprint(err)
                    # когда сериализатор пытается найти переменную
                    ...
                finally:
                    ...

    def print_compiled_message(self):
        width = self.max_len
        if self.compilied_message:
            console_dict.print(self.compilied_message, width=width)

    def print_obj(self):
        width = self.max_len
        if self.obj:
            console_dict.print(
                self.obj,
                style="green",
                width=width,
                markup=True,
            )  # !!!
            return


logger.remove()


def format_exception(record):
    message = record.get("message")
    line = record.get("line")
    level = record.get("level")
    file = record.get("file")
    msg = print_tbl(
        level=level,
        message=message,
        file=file,
        line=line,
        style="error"
        # style="error_msg"
    )
    record["extra"]["msg"] = msg
    return config.LOGURU_EXCEPTION_FORMAT_LONG


def format_regular_msg(record):
    message = record.get("message")
    line = record.get("line")
    level = record.get("level")
    obj = record.get("extra").get("o")
    # print("=" * 20)
    # print(type(obj))
    # print("=" * 20)
    file = record.get("file")
    msg = print_tbl(
        level=level,
        message=message,
        file=file,
        line=line,
        # style=f"{level.name.lower()}"
        style=level.name.lower()
        # style="debug"
        # style="error_msg"
    )
    record["extra"]["msg"] = msg
    # with console.capture() as capture:
    #     console_dict.print(obj, markup=True, width=75)
    # return capture.get()
    # obj_in_tbl = print_tbl_obj(
    #     level=level, message=obj, file=file, line=line, style=f"{level.name.lower()}"
    # )
    # record["extra"]["obj"] = obj_in_tbl
    # record["extra"]["obj"] = capture.get()
    # return "{extra[obj]}"
    # return "{extra[msg]}\n{extra[obj]}"
    # record["extra"]["obj"] = obj
    if obj:
        record["extra"]["obj"] = ccapt(obj)
        return "{extra[msg]}\n{extra[obj]}"
    return "{extra[msg]}"
    # return "{extra[msg]}\n{extra[serialized]}\n"
    # return config.LOGURU_GENERIC_FORMAT


logger.level("foobar", no=33, icon="🤖", color="<blue>")

from functools import partialmethod


def serialize(record):
    subset = {"timestamp": record["time"].timestamp(), "message": record["message"]}
    return json.dumps(subset)


def sink(message):
    serialized = serialize(message.record)
    print(serialized)


# для всех записей кроме исключений
logger.add(
    # sink=print,
    # print,
    sink=sys.stdout,
    # sink=sink,
    # pprint,
    # console_dict.log,
    # console_dict.print,
    # sink=MySynk,
    level=config.LOG_LEVEL,
    format=format_regular_msg,
    # format=config.LOGURU_GENERIC_FORMAT,
    backtrace=False,
    catch=False,
    filter=lambda record: record["extra"].get("name") == "all",
)

extra = None


def sinko(message):
    # nonlocal extra
    print(type(message))
    extra = message.record["extra"]


# logger.add(
#     sink=sinko,
#     # sink=sys.stdout,
#     # level=config.LOG_LEVEL,
#     # format=format_regular_msg,
#     # format=config.LOGURU_GENERIC_FORMAT_OBJ,
#     # backtrace=False,
#     # catch=False,
#     # filter=lambda record: record["extra"].get("name") == "obj",
# )


# logger = logger.patch(
#     lambda record: record.update(message=record["extra"].get("o", record["message"]))
# )

# только для исключений
# сначала работает synk, затем форматтер
logger.add(
    sys.stderr,
    filter=lambda record: record["extra"].get("name") == "err",
    format=format_exception,
    backtrace=False,
    catch=True,
    # diagnose=False,
)


def patching(record):
    message = record["message"]
    obj = record["extra"].get("o")
    # print(5555555555555)
    print(type(record))
    # try:
    #     record.update(message=eval(message))
    # except Exception:
    #     ...
    # if obj:
    #     record.update(message=ccapt(obj))
    if not isinstance(message, str):
        print(777777777777)
        # record["extra"]["o"] = message
        # record.update(message=record["extra"].get("o", record["message"]))
    # record["extra"]["serialized"] = record["message"]


# logger = logger.patch(patching)

errlog = logger.opt(colors=True, exception=True, record=False).bind(name="err")
# objlog = logger.opt(colors=True, exception=True, record=False).bind(obj=True)


# log = func()

log_ = logger.opt(record=False, colors=True, raw=False).bind(name="all")

# logo = logger.opt(record=True, raw=True).bind(name="obj")
# run = True


def func(
    *args,
    # first_run=False,
    **kwargs,
):
    # print("+" * 20)
    # init =
    # print(first_run)
    # print(type(args[2]))
    # if first_run:
    #     run=False
    # if not run:
    #     return
    print(args)
    print(kwargs)
    if isinstance(args[2], dict):
        return getattr(log, args[1])("", o=args[2])
    obj = kwargs.get("o")

    if obj:
        return getattr(log, args[1])(args[2], o=obj)

    return getattr(log, args[1])(args[2])
    # return log.debug(args[2])
    # return logger.__class__.log
    # return logger.opt(record=False, colors=True, raw=False).bind(name="all")


# logger.__class__.debug = partialmethod(logger.__class__.log, "foobar", "*args")
# logger.__class__.foobar = partialmethod(func, "debug")
# log.__class__.debug = partialmethod(
#     func,
#     "debug",
# first_run=True,
# init2=True,
# )


def print_log(level, *args, **kwargs):
    if isinstance(args[0], dict):
        return getattr(log_, level)("", o=args[0])
    obj = kwargs.get("o")

    if obj:
        return getattr(log_, level)(args[0], o=obj)

    return getattr(log_, level)(args[0])


class Logger:
    # @staticmethod

    # @classmethod
    @staticmethod
    def debug(*args, **kwargs):
        print_log("debug", *args, **kwargs)

    @staticmethod
    def trace(*args, **kwargs):
        print_log("trace", *args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        print_log("info", *args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        print_log("warning", *args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        print_log("error", *args, **kwargs)

    @staticmethod
    def critical(*args, **kwargs):
        print_log("critical", *args, **kwargs)

        # print(args)
        # print("-" * 20)
        # print(kwargs)
        # print("=" * 20)
        # return

        # return log.debug(*args, **kwargs)


log = Logger()
