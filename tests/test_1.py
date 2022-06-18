# import pytest
# import rich
# from rich.traceback import install
#
# # install(show_locals=True)
#
#
# from logger.config import config
# from logger.logger_ import log
#
#
# # @rich.catch
# def func():
#     return 1 / 0
#
#
# @log.catch
# def del_zero(arg):
#     return arg / 0
#
#
# @pytest.mark.skip
# def test_one():
#     str_ = "1234567890"
#     log.debug(f"{config.LOG_LEVEL=}")
#     log.debug(str_)
#     log.trace(str_)
#     log.success(str_)
#     log.warning(str_)
#     log.info(str_)
#     log.critical(str_)
#
#
# @pytest.mark.skip
# def test_too():
#     # @log.catch(message="Because we never know...")
#     # install(show_locals=True)
#
#     t = 1
#     # func()
#     del_zero(5)
#
#
# # del_zero(5)
# # log.exception("wtf?")
#
#
# def func2(a, b):
#     return a / b
#
#
# def nested(c):
#     try:
#         func2(5, c)
#     except ZeroDivisionError:
#         log.exception("What?!")
#
#
# nested(0)
