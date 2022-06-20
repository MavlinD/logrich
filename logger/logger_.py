import sys
from typing import NamedTuple

import stackprinter
from loguru import logger, _handler
from rich.errors import MissingStyle, MarkupError
from rich.pretty import pprint
from rich.table import Table
from rich.console import Console

from logger.color_scheme import MyReprHighlighter, theme
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


console = Console()

console_dict = Console(
    highlighter=MyReprHighlighter(),
    theme=theme,
    markup=True,
    log_time=False,
    log_path=False,
)


class FirstLine(NamedTuple):
    """первая строка лога"""

    level: str
    message: str
    source: str


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
        self.print_log_header()
        self.print_compiled_message()
        self.print_obj()
        if print_rule:
            console.rule(style="#33adff")

    def print_log_header(self) -> None:
        """печатает строку уровня - заголовок лога"""
        first = self.log_entry.replace("%level%", f"[{self.level}]").replace("\n", "")
        parts = first.split("%%")
        self.print_first(FirstLine(level=parts[0], message=self.message, source=parts[1]))

    @property
    def message(self) -> str:
        if len(self._message) < self.max_len:
            return self._message
        if self.compilied_message:
            return ""
        return self._message

    def print_first(self, first_line: FirstLine):
        """печать сообщения"""
        style = f"{self.level}_msg"
        try:
            table = Table(
                highlight=True,
                show_header=False,
                padding=0,
                collapse_padding=True,
                show_edge=False,
                show_lines=False,
                show_footer=False,
                expand=True,
                box=None,
            )
            table.add_column(justify="left", min_width=config.MIN_WIDTH, max_width=config.MAX_WIDTH)
            table.add_column(ratio=config.RATIO_MAIN, overflow="fold", style=style)
            table.add_column(justify="right", ratio=config.RATIO_FROM, overflow="fold")
            table.add_column(ratio=2, overflow="crop")  # для паддинга справа

            table.add_row(f"{first_line.level}", f"{first_line.message}", f"{first_line.source}")

            console_dict.print(table)

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
                    self.compilied_message = eval(self._message)
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

# для всех записей кроме исключений
logger.add(
    sink=MySynk,
    level=config.LOG_LEVEL,
    format=config.LOGURU_GENERIC_FORMAT,
    backtrace=False,
    catch=False,
    filter=lambda record: record["extra"].get("name") == "all",
)


def format2(record):
    # format_ = "{time} {message}\n"
    format_ = config.LOGURU_EXCEPTION_FORMAT + "\n"
    # stackprinter.set_excepthook(style="darkbg2")
    print("=" * 20)
    # print(record["exception"])
    # print(type(record["exception"]))  # loguru._recattrs.RecordException
    # print("=" * 20)

    if record["exception"] is not None:
        # record["extra"]["stack"] = stackprinter.format(record["exception"])
        # record["extra"]["stack"] = 'stackprinter.format(record["exception"])'
        ...
        # stackprinter.show(record["exception"], style="darkbg2")
        format_ += "{stack}\n"
        # format_ += "{extra[stack]}\n"

    # return record["exception"]
    return format_


def format4(record):
    # format_ = "{time} {message}\n"
    # return repr(record)
    return config.LOGURU_EXCEPTION_FORMAT


def format3(record):
    # format_ = "{time} {message}\n"
    format_ = config.LOGURU_EXCEPTION_FORMAT + "\n"
    # stackprinter.set_excepthook(style="darkbg2")

    if record["exception"] is not None:
        record["extra"]["stack"] = stackprinter.format(record["exception"])
        # record["extra"]["stack"] = record["exception"]
        # sys.stderr.write(repr(record["exception"]))
        # sys.stderr.write(sys.exc_info())
        format_ += "{extra[stack]}\n"

    return format_


class ExcSynk:
    max_len = config.MAX_WITH_LOG_OF_OBJ
    compilied_message = None
    is_printed_compile_message = False
    is_compile_error = None

    def __init__(self, record):
        # https://docs-python.ru/standart-library/modul-sys-python/obekty-stdin-stdout-stderr-modulja-sys/
        # def __init__(self, log_entry: _handler.Message):
        # def __init__(self, *arg, **kwargs):
        """печатает запись лога"""
        # self.log_entry = log_entry

        # https://rich.readthedocs.io/en/stable/_modules/rich/highlighter.html
        # https://rich.readthedocs.io/en/stable/highlighting.html
        # https://loguru.readthedocs.io/en/stable/resources/recipes.html#serializing-log-messages-using-a-custom-function

        # self.level = self.log_entry.record["level"].name.lower()
        # self.obj = self.log_entry.record.get("extra").get("o")
        # print_rule = self.log_entry.record.get("extra").get("rule")
        # self._message = self.log_entry.record["message"]
        # return sys.stdout
        # print(repr(arg))
        # print(exception)
        # print(repr(kwargs))
        # sys.stderr.write(exception)
        # import stackprinter
        # stackprinter.set_excepthook(style="darkbg2")
        # stackprinter.show()
        # stackprinter.show(style="darkbg", source_lines=4)

        # sys.stdout.write(record) # уже отформатированное stackprinter, но без цвета
        # t = console_dict.render(record)
        # t = console_dict.render_str(record)
        # print(record)
        # sys.stderr.flush()
        console.print(record)
        # sys.stderr.write(record)
        # console_dict.print(record)
        # console_dict.log(record)
        # sys.stdout.write(record["exception"])
        ...
        # self.restore_message()
        # self.print_log_header()
        # self.print_compiled_message()
        # self.print_obj()
        # if print_rule:
        #     console.rule(style="#33adff")


import traceback
from itertools import takewhile


def tracing_formatter(record):
    # Filter out frames coming from Loguru internals
    frames = takewhile(lambda f: "/loguru/" not in f.filename, traceback.extract_stack())
    stack = " > ".join("{}:{}:{}".format(f.filename, f.name, f.lineno) for f in frames)
    record["extra"]["stack"] = stack
    return "{level} | {extra[stack]} - {message}\n{exception}"


def print_tbl(level, message, file, line, style=None):
    table = Table(
        highlight=True,
        show_header=False,
        padding=0,
        collapse_padding=True,
        show_edge=False,
        show_lines=False,
        show_footer=False,
        expand=True,
        box=None,
    )
    table.add_column(justify="left", min_width=config.MIN_WIDTH, max_width=config.MAX_WIDTH)
    # table.add_column(ratio=config.RATIO_MAIN, overflow="fold")
    table.add_column(ratio=config.RATIO_MAIN, overflow="fold", style="error_msg")
    table.add_column(justify="right", ratio=config.RATIO_FROM, overflow="fold")
    table.add_column(ratio=2, overflow="crop")  # для паддинга справа

    # table.add_row(None, f"{message}", f"{'first_line.source'}")
    # table.add_row(None, f"{message}", None)
    table.add_row(
        f"[red bold reverse] {level:<8}[/]",
        f"{message}",
        f"[#858585]{file}...[/][#eb4034]{line}[/]",
    )
    # console_dict.print(table)
    # return table
    with console.capture() as capture:
        # console.print("[bold magenta]Hello World[/]")
        console_dict.print(table)
    res = capture.get()
    # pprint(capture.get())
    return res


LOGURU_EXCEPTION_FORMAT_LONG: str = (
    # "<lvl><v><r> {level:<7} </></></lvl>{extra[msg]}<fg #858585>{file:>112}...</>"
    # "<fg #eb4034>{line}</>\n{exception}"
    "{extra[msg]}\n{exception}"
)


class Formatter:
    def __init__(self):
        self.padding = 0
        # self.fmt = "{time} | {level: <8} | {name}:{function}:{line}{extra[padding]} | {message}\n{exception}"
        self.fmt = config.LOGURU_EXCEPTION_FORMAT + "\n{exception}"

    # self.fmt = config.LOGURU_EXCEPTION_FORMAT + "\n" + "{message}\n{exception}"

    def format(self, record):
        # length = len("{name}:{function}:{line}".format(**record))
        message = record.get("message")
        line = record.get("line")
        level = record.get("level")
        file = record.get("file")
        msg = print_tbl(level, message, file, line)
        # msg = print_tbl(message, None)
        record["extra"]["msg"] = msg
        return LOGURU_EXCEPTION_FORMAT_LONG
        return config.LOGURU_EXCEPTION_FORMAT
        # length_msg = len(message)
        # if length_msg > config.MAX_WITH_LOG_OF_OBJ:
        #     self.fmt = (
        #         LOGURU_EXCEPTION_FORMAT_LONG
        #         + "\n{extra[msg]}\n{exception}"
        #         # + "\n<lvl><n>{message:->80}</></>\n{extra[msg]}\n{exception}"
        #     )

        # self.padding = max(self.padding, length)
        # record["extra"]["padding"] = " " * (self.padding - length)
        # return self.fmt


formatter = Formatter()


# только для исключений
# сначала работает synk, затем форматтер
logger.add(
    # sys.stdout,
    # ExcSynk,
    sys.stderr,
    # stackprinter.format,
    filter=lambda record: record["extra"].get("name") == "err",
    # format=config.LOGURU_EXCEPTION_FORMAT,
    # format=format3,
    # format=format4,
    format=formatter.format,
    # format=tracing_formatter,
    # format=format2,
    backtrace=False,
    catch=False,
)

# errlog = logger.bind(name="err")
# errlog = logger.opt(colors=True, exception=False).bind(name="err")
errlog = logger.opt(colors=True, exception=True, record=False).bind(name="err")

log = logger.bind(name="all")
