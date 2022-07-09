from logrich.logger_ import errlog, log


# @errlog.catch
@errlog.catch(message="Because we never know...O_o.\nДемонстрация вывода исключений.")
def del_zero(arg):
    return arg / 0


obj = {
    "name": "Имя, фамилия " * 5,
    "slug": 759933327936516,
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


def test_too():
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
