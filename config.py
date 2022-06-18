import os
from pydantic import BaseSettings

BASE_DIR = os.path.dirname(__file__)

DOTENV_FILE = "./.env"


class Settings(BaseSettings):
    """
    Server config settings
    """

    class Config:
        env_file = DOTENV_FILE
        env_file_encoding = "utf-8"

    DEBUG: bool

    LOG_LEVEL: int = 0
    # макисмальная длина текста чтобы разместить его на одной линии с уровнем лога
    MAX_WITH_LOG_OF_OBJ: int = 120
    LOGURU_FORMAT: str = "%level% {level:<7} [/]%%[#858585]{file}...[/][#eb4034]{line}[/]"


config = Settings()
