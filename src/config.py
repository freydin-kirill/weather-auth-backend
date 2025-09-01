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

    # RabbitMQ
    RABBITMQ_HOST: str = Field("localhost", env="RABBITMQ_HOST")
    RABBITMQ_PORT: int = Field(5672, env="RABBITMQ_PORT")
    RABBITMQ_USER: str = Field("guest", env="RABBITMQ_USER")
    RABBITMQ_PASS: str = Field("guest", env="RABBITMQ_PASS")
    RABBITMQ_VHOST: str = Field("/", env="RABBITMQ_VHOST")
    RABBITMQ_EXCHANGE: str = Field("weather.exchange", env="RABBITMQ_EXCHANGE")
    RABBITMQ_QUEUE: str = Field("weather.current.queue", env="RABBITMQ_QUEUE")
    RABBITMQ_ROUTING_KEY: str = Field("weather.current", env="RABBITMQ_ROUTING_KEY")

    @property
    def db_url_async(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
