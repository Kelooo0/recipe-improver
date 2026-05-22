from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    SECRET_KEY: str
    API_KEY: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    ALGORITHM: str = "HS256"
    BANNED: set[str] = {
        "null",
        "none",
        "true",
        "false",
        "undefined",
        "object",
        "array",
        "select",
        "insert",
        "update",
        "delete",
        "drop",
        "union",
        "script",
        "test",
        "asd",
        "asdf",
        "qwerty",
        "foo",
        "bar",
        "baz",
    }

    @property
    def DATABASE_URL(self) -> str:
        pw = quote_plus(self.DB_PASS)
        return f"postgresql://{self.DB_USER}:{pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
