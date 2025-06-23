from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".." / ".env")

    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(..., env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASS: str = Field(..., env="DB_PASS")

    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    OPEN_METEO_API_URL: str = Field(..., env="OPEN_METEO_API_URL")

    METEO_SOURCE_API_KEY: str = Field(..., env="METEO_SOURCE_API_KEY")
    METEO_SOURCE_API_URL: str = Field(..., env="METEO_SOURCE_API_URL")

    TOMORROW_IO_REALTIME_API_URL: str = Field(..., env="TOMORROW_IO_REALTIME_API_URL")
    TOMORROW_IO_FORECAST_API_URL: str = Field(..., env="TOMORROW_IO_FORECAST_API_URL")
    TOMORROW_IO_API_KEY: str = Field(..., env="TOMORROW_IO_API_KEY")

    @property
    def db_url_async(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
