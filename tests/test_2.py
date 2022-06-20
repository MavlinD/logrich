from pprint import pprint

import pytest

# from rich.traceback import install

# install(show_locals=True)
import stackprinter

from logger.logger_ import errlog

# from logger.logger_ import log


# @errlog.catch
t = 899

# @errlog.catch(message="Ой вэй, а мы и не знали...")
@errlog.catch(message="a" * 160)
def del_zero(arg):
    return arg / 0


def del_zero2(arg):
    try:
        pprint(arg)
        return arg / 0
    except Exception as err:
        # sys.exc_info()
        # pprint(err)
        ...
        # stackprinter.format(err)


# del_zero(77)


def test_too():
    # def test_too(caplog):
    i = 98991
    del_zero(5)
    # log.debug("a" * 160)
    # str_ = "160" * 61
    # log.debug(str_)

    # del_zero2(555555)
