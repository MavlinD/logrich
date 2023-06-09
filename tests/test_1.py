import pytest
from rich.style import Style

from logrich import errlog, log, console

TEST = "[reverse grey70] TEST     [/]"
log.level(TEST, no=15)
log.test = lambda msg: log.log(TEST, msg)  # type: ignore


# @errlog.catch
@errlog.catch(message="Because we never know...O_o.\nДемонстрация вывода исключений.")
def del_zero(arg):
    return arg / 0


obj = {
    "name": "Имя, фамилия " * 5,
    "slug": 7599333279365,
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
    "access": "eyJ0eXAiiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzNTUwMTY1LCJqdGkiOiJmNzFhYjg5OWE5MDY0Y2EwODgwMzY1NzQ1NjYwNzdjOSIsInVzZXJfaWQiOjF9.KES3fhmBTXy8AwDSJTseNsLFC3xSh1J_slndgmSwp08",
    "id": 1234561,
}


# @rich.repr.auto
# декоратор формирует __repr_rich__ на основе __init__ объекта
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


# @pytest.mark.skip
def test_one():
    log.trace("Сообщение уровня TRACE: 5")
    log.debug("Сообщение уровня DEBUG: 10")
    log.info("Сообщение уровня INFO: 20")
    log.success("Сообщение уровня SUCCESS: 25")
    log.warning("Сообщение уровня WARNING: 30")
    log.error("Сообщение уровня ERROR: 40; " * 10)
    log.critical(
        "Это катастрофа, парень шел к успеху, но не фартануло..:-(\nСообщение уровня CRITICAL: 50"
    )
    log.debug("Объект птички", o=BIRDS)
    log.info("Словарь", o=obj)
    # return
    log.success("SUCCESS [#FF1493]SUCCESS[/] [#00FFFF]SUCCESS[/] " * 10)
    del_zero(5)
    log.debug("=" * 70)

    title = "Это Спарта!"
    console.rule(f"[green]{title}[/]", style=Style(color="magenta"))

    num_dict = {1: {2: {2: 111}, 3: {3: 111}}, 2: {3: {3: 111}}, 3: {2: {2: 111}, 3: {3: 111}}}
    log.debug("неверно раскрашивает первые числа", o=num_dict)
    num_dict = {
        1: {2: {2: "здесь будут стили"}, 3: {3: "здесь будут стили"}},
        2: {3: {3: "здесь будут стили"}},
        3: {2: {2: "здесь будут стили"}, 3: {3: "здесь будут стили"}},
    }
    log.debug("неверно раскрашивает первые двойки", o=num_dict)

    context = {"clientip": "192.168.0.1", "user": "fbloggs"}

    # logger.info("Protocol problem", extra=context)  # Standard logging
    # logger.bind(**context).info("Protocol problem")  # Loguru


def test_too():
    log.log("INFO", "test-")
    # TEST = log.level("TEST")
    # TST = "<red>TST"
    # TST = "TST"
    # TST = "[reverse gray70] TST      [/]"
    # TST = "[reverse yellow] TST      [/]"
    # log.level(TST, no=15)
    # log.level(TST, no=15, style="red")
    # log.log(TST, "Тестовый лог")
    # log.tst = lambda msg: log.log(TST, msg)
    log.test("Тестовый лог")
    # log.log(TEST, "test-2")
