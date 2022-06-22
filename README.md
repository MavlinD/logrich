###Логгер

####Совместная работа [loguru](https://loguru.readthedocs.io) & [rich](https://rich.readthedocs.io).

![Screenshot logger](wiki/screenshot_logger.png?raw=True)

Уровень вывода исключений определяется в переменных окружения.
Цвета, ширины и шаблоны вывода также могут быть определены в окружении.

Обработчики записей логов можно определять дополнительно, например запись в файл или отправка в канал.

#### Как развернуть:

```shell
git clone 
cd logger_mdv
poetry shell
poetry install
```

#### Запустить тест(ы):

```shell
pytest
# монитор тестов
ptw
```
