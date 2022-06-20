from pprint import pprint

import pytest

# from rich.traceback import install

# install(show_locals=True)
# import stackprinter

from logger.logger_ import errlog
from logger.logger_ import log


# @errlog.catch
t = 899

# @errlog.catch(message="Ой вэй, а мы и не знали...")
@errlog.catch(message="a" * 160)
def del_zero(arg):
    y = 9
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
    i = 98991718777
    log.debug("m" * 16)
    del_zero(5)
    log.debug("a" * 160)
    str_ = "у " * 61
    log.debug(str_)
    str_ = "a" * 161
    log.debug(str_)

    # del_zero2(555555)
