from pprint import pprint

import pytest

from logger.logger_ import errlog
from logger.logger_ import log


# @errlog.catch
# @errlog.catch(message="a=" * 160)
@errlog.catch(message="Ой вэй, а мы и сами про это мы не знали...O_o")
def del_zero(arg):
    return arg / 0


def del_zero2(arg):
    try:
        pprint(arg)
        return arg / 0
    except Exception as err:
        ...


# @rich.repr.auto
obj = {
    "name": "Имя, просто имя " * 5,
    "slug": 753951,
    "slug1": 1,
    "slug2": 51,
    "slug-test": 198,
    "slug3": 951,
    "href": "http://0.0.0.0:8000/downloads/pf-pf4-2050596-e4b8eff7.xlsx",
    "digest": "e4b8eff72593c54e40a3f0dfa3aff156",
    "message": "File pf-pf4-2050596-e4b8eff7 created now",
    "score": 123456,
    "elapsed_time": "0.060 seconds",
    "version": "2.14.3",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzNTUwMTY1LCJqdGkiOiJmNzFhYjg5OWE5MDY0Y2EwODgwMzY1NzQ1NjYwNzdjOSIsInVzZXJfaWQiOjF9.KES3fhmBTXy8AwDSJTseNsLFC3xSh1J_slndgmSwp08",
    "id": 1234561,
}


# @rich.repr.auto
class Bird:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct

    def __repr__(self):
        return f"Bird({self.name}, eats={self.eats!r}, fly={self.fly!r}, extinct={self.extinct!r})"


BIRDS = {
    "gull": Bird("gull", eats=["fish", "chips", "ice cream", "sausage rolls"]),
    "penguin": Bird("penguin", eats=["fish"], fly=False),
    "dodo": Bird("dodo", eats=["fruit"], fly=False, extinct=True),
}


def test_too():
    i = 914783

    log.debug("obj")

    log.debug(obj)
    return
    log.trace("tst-obj", o=obj)
    log.warning("obj")
    log.error("err " * 100)
    log.critical(BIRDS)
    log.debug("===============++")
    # return
    log.debug("+++++9", o=obj)
    log.debug(obj)
    log.success("m" * 16)
    log.debug("a" * 160)
    str_ = "у " * 61
    log.debug(str_)
    str_ = "a" * 161
    log.info(str_)
    log.debug(str_)
    log.debug("", o=BIRDS)
    del_zero(5)
    log.critical("Ой вэй, всё пропало!")
    log.info("46464")
