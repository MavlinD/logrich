from typing import NamedTuple

from loguru import logger, _handler
from rich.errors import MissingStyle
from rich.highlighter import ReprHighlighter, _combine_regex as combine_regex
from rich.pretty import pprint
from rich.table import Table
from rich.theme import Theme
from rich.console import Console
from config import config

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


class MyReprHighlighter(ReprHighlighter):
    # https://regex101.com/r/zR2hP5/1
    base_style = "repr."
    highlights = [
        r"(?<![\\\w])(?P<str>b?'''.*?(?<!\\)'''|b?'.*?(?<!\\)'|b?\"\"\".*?(?<!\\)\"\"\"|b?\".*?(?<!\\)\")",
        r":\s\'(?P<value>.+)\'",
        r"['](?P<string_list_tuple>\w+)[']",
        r"(?P<digit2>\d*)[\"\s,[,(](?P<digit>\d*\.?\s?-?\d*-?\.?\d+)",
        combine_regex(
            r"(?P<brace>[][{}()])",
            r"\'(?P<key>[\w-]+)\'(?P<colon>:)",
            r"(?P<comma>,)\s",
        ),
        r"(?P<quotes>\')",
        r"(?P<equal>=)",
        r"(?P<class_name>[A-Z].*)\(",
        r'(?P<attrib_name>[\w_]{1,50})=(?P<attrib_value>"?[\w_]+"?)?',
        r"\b(?P<bool_true>True)\b|\b(?P<bool_false>False)\b|\b(?P<none>None)\b",
    ]


color_of_digit = "bold magenta"

theme = Theme(
    # https://www.w3schools.com/colors/colors_picker.asp
    # https://htmlcolorcodes.com/color-names/
    # https://colorscheme.ru/
    {
        "repr.brace": "bold black",
        "repr.str": "green",
        # "repr.str": "dim bold blue",
        # "repr.call": "dim bold blue",
        "repr.attrib_name": "#0099ff",
        "repr.equal": "red dim",
        # "repr.attrib_name": "#00ff00",
        # "repr.attrib_value": "dim bold red",
        # "repr.bool_true": "dim bold blue",
        # "repr.tag_start": "dim bold blue",
        "repr.digit": color_of_digit,
        "repr.digit2": color_of_digit,
        "repr.colon": "#D2691E",
        "repr.quotes": "#778899",
        "repr.comma": "#778899",
        "repr.key": "#08e8de",
        "repr.bool_true": "bold blue",
        "repr.none": "blue",
        "repr.bool_false": "yellow",
        "repr.class_name": "magenta bold",
        # "repr.value": "dim bold blue",
        # "repr.value": "green",
        "repr.string_list_tuple": "green",
        "trace": "reverse #0b66de",
        "trace_msg": "#05a7f7",
        "debug": "#182D0B on #9F2844",
        # "debug": "reverse #7B3F00",
        "debug_msg": "#e64d00",
        "info": "reverse blue",
        "info_msg": "#33ccff",
        "success": "reverse green",
        "success_msg": "green",
        "warning": "reverse yellow",
        "warning_msg": "yellow",
        "error": "reverse #b00bde",
        "error_msg": "#b00bde",
        "critical": "reverse #de0b2e",
        "critical_msg": "#de0b2e",
    }
)

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
            table.add_column(justify="left", min_width=12, max_width=15)
            table.add_column(ratio=80, overflow="fold", style=style)
            table.add_column(justify="right", ratio=40, overflow="fold")
            table.add_column(ratio=2, overflow="crop")  # для паддинга справа
            table.add_row(f"{first_line.level}", f"{first_line.message}", f"{first_line.source}")
            # pprint(table)
            console_dict.print(table)
        except MissingStyle:
            pprint(f"Стиль {style} не найден")

    def restore_message(self):
        """пытается сериализовать основное тело записи лога"""
        if not self.obj:
            if len(self._message) >= self.max_len:
                try:
                    self.compilied_message = eval(self._message)
                except SyntaxError as err:
                    pprint(err)
                    self.is_compile_error = True
                    # вероятно это строка
                    ...
                except NameError as err:
                    pprint(err)
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

logger.add(
    sink=MySynk,
    level=config.LOG_LEVEL,
    format=config.LOGURU_FORMAT,
    backtrace=False,
)

log = logger
