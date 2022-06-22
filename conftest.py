import sys
from typing import Generator

from _pytest import nodes
from _pytest.config import Config
from _pytest.config.argparsing import Parser

from loguru import logger
from _pytest.logging import LogCaptureFixture

import pytest
import logging

from nice_logger.logger_assets import console
from nice_logger.config import config as config_


def pytest_addoption(parser: Parser) -> None:
    """Add a command line option to disable nice_logger."""
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


@pytest.fixture
def caplog(caplog: LogCaptureFixture) -> Generator:
    # https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog
    # https://florian-dahlitz.de/articles/logging-made-easy-with-loguru#wait-there-is-more
    logger.remove()
    handler_id = logger.add(
        sys.stdout,
        level=config_.LOG_LEVEL,
        format=config_.LOGURU_EXCEPTION_FORMAT_LONG,
        backtrace=False,
    )
    yield caplog
    logger.remove(handler_id)
