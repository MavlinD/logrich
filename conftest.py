import sys

from _pytest.nodes import Item

from loguru import logger
from _pytest.logging import LogCaptureFixture

import pytest
import logging

from logger.config import config
from logger.logger_ import console


def pytest_addoption(parser):
    """Add a command line option to disable logger."""
    parser.addoption("--log-disable", action="append", default=[], help="disable specific loggers")
    parser.addoption("--cmdopt", action="store", default="type1", help="my option: type1 or type2")


def pytest_runtest_call(item: Item):
    # https://docs.pytest.org/en/6.2.x/reference.html
    console.rule(f"[green]{item.parent.name}[/]::[yellow bold]{item.name}[/]")


def pytest_configure(config):
    """Disable the loggers."""
    for name in config.getoption("--log-disable", default=[]):
        logger = logging.getLogger(name)
        logger.propagate = False
    called_from_test = True


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    # https://localcoder.org/run-code-before-and-after-each-test-in-py-test
    print()
    yield


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    # https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog
    # https://florian-dahlitz.de/articles/logging-made-easy-with-loguru#wait-there-is-more
    # handler_id = logger.add(caplog.handler)
    logger.remove()
    handler_id = logger.add(
        sys.stdout,
        level=config.LOG_LEVEL,
        format=config.LOGURU_EXCEPTION_FORMAT,
        backtrace=False,
    )
    yield caplog
    logger.remove(handler_id)
