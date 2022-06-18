import pytest

# from rich.traceback import install

# install(show_locals=True)


from logger.logger_ import log, errlog


# @errlog.catch
t = 999941211125491959


# @errlog.catch(message="Ой вэй, а мы и не знали...")
@errlog.catch(message="a" * 160)
def del_zero(arg):
    return arg / 0


# del_zero(77)


def test_too():
    # def test_too(caplog):

    del_zero(5)
    log.debug("a" * 160)
