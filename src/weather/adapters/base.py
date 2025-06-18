from abc import ABC, abstractmethod

from httpx import AsyncClient

from src.weather.enums import SchemaMode
from src.weather.schemas.base import BaseWeatherSchema


async def send_weather_request(url, params) -> dict:
    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


class BaseWeatherAdapter(ABC):
    _url: str
    _params: dict[str, str | int | list[str | float]]

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_write_schema(cls) -> type[BaseWeatherSchema]:
        pass

    @classmethod
    @abstractmethod
    def get_response_schema(cls, mode: SchemaMode) -> type[BaseWeatherSchema]:
        pass

    @classmethod
    @abstractmethod
    async def fetch_current_weather(cls, latitude: float, longitude: float, **kwargs) -> dict:
        pass

    @classmethod
    @abstractmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        pass
