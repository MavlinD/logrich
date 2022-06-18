# import rich
# from rich.traceback import install

# install(show_locals=True)


from logger.logger_ import log, errlog


# @errlog.catch
@errlog.catch(message="Because we never know...")
def del_zero(arg):
    return arg / 0


del_zero(77)
log.debug(433434344)
