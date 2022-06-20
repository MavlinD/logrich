# import rich
# from rich.traceback import install

# install(show_locals=True)
from pprint import pprint

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

# from logger.logger_ import log, errlog


# @errlog.catch
# @errlog.catch(message="Because we never know...")
# def del_zero(arg):
#     return arg / 0


# del_zero(77)
# log.debug(433434344)


def del_zero2(arg):
    try:
        # pprint(arg)
        return arg / 0
    except Exception as err:
        # sys.exc_info()
        # pprint(err)
        ...
        # stackprinter.format()
        # stackprinter.show()
        # stackprinter.show(style='darkbg2', source_lines=4)
        stackprinter.show(style="darkbg2")
        # stackprinter.format(err)


del_zero2(9999)
