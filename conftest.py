from typing import Generator

from _pytest import nodes
from _pytest.config import Config
from _pytest.config.argparsing import Parser


import pytest
import logging
from logrich.app import console


def pytest_addoption(parser: Parser) -> None:
    """Add a command line option to disable logrich."""
    parser.addoption("--log-disable", action="append", default=[], help="disable specific loggers")
    parser.addoption("--cmdopt", action="store", default="type1", help="my option: type1 or type2")


def pytest_runtest_call(item: nodes.Item) -> None:
    # https://docs.pytest.org/en/6.2.x/reference.html
    console.rule(f"[green]{item.parent.name}[/]::[yellow bold]{item.name}[/]")  # type: ignore


def pytest_configure(config: Config) -> None:
    """Disable the loggers."""
    for name in config.getoption("--log-disable", default=[]):
        logger_ = logging.getLogger(name)
        logger_.propagate = False


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir) -> Generator:
    """Fixture to execute asserts before and after a test is run"""
    # https://localcoder.org/run-code-before-and-after-each-test-in-py-test
    print()
    yield
