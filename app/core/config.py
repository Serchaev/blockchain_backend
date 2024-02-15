from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR.joinpath(".env"),
    )
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_NAME_TEST: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PREFIX: str
    MODE: Literal["DEV", "PROD", "TEST"]

    @property
    def db_url(self) -> str:
        if self.MODE == "DEV":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"  # noqa
        if self.MODE == "TEST":
            return f"postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"  # noqa
        if self.MODE == "PROD":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"  # noqa

    @property
    def db_echo(self) -> bool:
        if self.MODE == "PROD":
            return False
        return True


settings = Setting()

if __name__ == "__main__":
    print(BASE_DIR)
