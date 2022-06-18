from config import config
from logger.logger_ import log


def test_one():
    log.debug(654654646)
    log.trace(65465464226)
    log.debug(65465464226)
    log.success(65465464226)
    log.warning(65465464226)
    log.debug("", o=config)
    log.debug(config)
    log.critical(65465464226)
