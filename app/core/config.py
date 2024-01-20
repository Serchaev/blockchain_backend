from pathlib import Path

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
    MODE: str

    @property
    def db_url(self) -> str:
        if self.MODE == "DEV":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        if self.MODE == "TEST":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/test_{self.DB_NAME}"
        if self.MODE == "PROD":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def db_echo(self) -> bool:
        if self.MODE == "PROD":
            return False
        return True


settings = Setting()

if __name__ == "__main__":
    print(BASE_DIR)
