# import pytest
# import rich

# from loguru import logger
# from rich.traceback import install

# install(show_locals=True)


# from logger.config import config
# from logger.logger_ import log


# @rich.catch
def func():
    return 1 / 0


# @log.catch
# def del_zero(arg):
#     return arg / 0


def test_too():
    # @log.catch(message="Because we never know...")
    # install(show_locals=True)

    t = 1111545997992
    # func()
    # del_zero(5)

    def nested(c):
        from loguru import logger

        try:
            func2(5, c)
        except ZeroDivisionError:
            logger.exception("What?!")

    nested(0)


# del_zero(5)
# log.exception("wtf?")


def func2(a, b):
    return a / b
