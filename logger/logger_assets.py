from __future__ import annotations
import sys

import loguru

from rich.highlighter import ReprHighlighter, _combine_regex as combine_regex
from rich.theme import Theme
from rich.table import Table
from rich.console import Console
from logger.config import config


console = Console()


class MyReprHighlighter(ReprHighlighter):
    """подсветка вывода на основе регул. выражений"""

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
        "foobar": "reverse yellow",
        "foobar_msg": "yellow",
        "error": "red bold reverse",
        # "error": "reverse #b00bde",
        "error_msg": "#b00bde",
        "critical": "reverse #de0b2e",
        "critical_msg": "#de0b2e",
    }
)

theme_fmt = {
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
    "foobar": "reverse yellow",
    "foobar_msg": "yellow",
    "error": "red bold reverse",
    # "error": "reverse #b00bde",
    "error_msg": "#b00bde",
    "critical": "reverse #de0b2e",
    "critical_msg": "#de0b2e",
}

# инстанс консоли rich
console_dict = Console(
    highlighter=MyReprHighlighter(),
    theme=theme,
    markup=True,
    log_time=False,
    log_path=False,
    safe_box=True,
)


def print_tbl(
    level: loguru.RecordLevel, message: str, file: loguru.RecordFile, line: int, style: str
) -> str:
    """Форматирует вывод логгера в табличном виде"""
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
    # LEVEL
    table.add_column(
        justify="left",
        min_width=config.MIN_WIDTH,
        max_width=config.MAX_WIDTH,
    )
    # MESSAGE
    table.add_column(ratio=config.RATIO_MAIN, overflow="fold", style=f"{level.name.lower()}_msg")
    # FILE
    table.add_column(justify="right", ratio=config.RATIO_FROM, overflow="fold")
    # LINE
    table.add_column(ratio=2, overflow="crop")  # для паддинга справа

    table.add_row(
        f"[{theme_fmt.get(style)}] {level:<9}[/]",
        f"{message}",
        f"[#858585]{file}...[/][#eb4034]{line}[/]",
    )
    with console.capture() as capture:
        console_dict.print(table, markup=True)
    return capture.get()


def format_extra_obj_orig(message: object) -> str:
    """форматирует вывод исключений в цвете и в заданной ширине, исп-ся rich"""
    with console.capture() as capture:
        console_dict.print(message, markup=True, width=75)
        sys.stdout.write("\033[F")  # back to previous line
        # sys.stdout.write("\033[K")  # clear line
    return capture.get()


def format_extra_obj(message: object) -> str:
    """форматирует вывод исключений в цвете и в заданной ширине, исп-ся rich"""
    table = Table(
        padding=(0, 1),
        highlight=True,
        # show_header=False,
        # padding=0,
        # collapse_padding=True,
        # show_edge=False,
        # show_lines=False,
        show_footer=False,
        # expand=True,
        box=None,
    )
    # LEVEL
    # table.add_column(
    #     justify="left",
    #     min_width=3,
    #     max_width=3,
    # )

    table.add_column(
        # justify="right",
        # ratio=config.RATIO_MAIN,
        # overflow="fold",
    )

    def msg():
        # инстанс консоли rich
        console_dict2 = Console(
            # highlighter=MyReprHighlighter(),
            theme=theme,
            no_color=True,
            # markup=True,
            markup=False,
            log_time=False,
            log_path=False,
            safe_box=True,
            record=True,
            emoji=False,
            highlight=False,
        )

        with console_dict2.capture() as capture:
            console_dict2.print(
                message,
                markup=False,
                width=75,
                # markup=True,
                # no_color=True,
            )
            # sys.stdout.write("\033[F")  # back to previous line
            # sys.stdout.write("\033[K")  # clear line
        return capture.get()

    # MESSAGE

    table.add_row(
        "",
        f"{msg()}",
    )

    # FILE
    # return capture.get()

    with console.capture() as capture2:
        console_dict.print(table, markup=True)
    return capture2.get()
