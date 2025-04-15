from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE : Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL : Literal["DEBUG", "INFO"]

    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASS : str
    DB_NAME : str
    
    TEST_DB_HOST : str
    TEST_DB_PORT : int
    TEST_DB_USER : str
    TEST_DB_PASS : str
    TEST_DB_NAME : str

    SMTP_HOST : str
    SMTP_PORT : int
    SMTP_USER : str
    SMTP_PASS : str

    REDIS_PORT : int
    REDIS_HOST : str

    SECRET_KEY : str
    ALG : str

    model_config = SettingsConfigDict(env_file='.env')


    def get_database_url(self, string):
        self.DATABASE_URL = string
        return self


    def get_test_database_url(self, string):
        self.TEST_DATABASE_URL = string
        return self
    

Setting = Settings()

DATABASE_URL = f"postgresql+asyncpg://{Setting.DB_USER}:{Setting.DB_PASS}@{Setting.DB_HOST}:{Setting.DB_PORT}/{Setting.DB_NAME}"
TEST_DATABASE_URL = f"postgresql+asyncpg://{Setting.TEST_DB_USER}:{Setting.TEST_DB_PASS}@{Setting.TEST_DB_HOST}:{Setting.TEST_DB_PORT}/{Setting.TEST_DB_NAME}"
