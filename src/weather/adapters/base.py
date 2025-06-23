from abc import ABC, abstractmethod

from httpx import AsyncClient

from src.weather.schemas.base import BaseWeatherSchema
from src.weather.utils.enums import ProvidersMode


async def send_weather_request(url, params) -> dict:
    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


class BaseWeatherAdapter(ABC):
    @classmethod
    @abstractmethod
    def url(cls, **kwargs) -> str:
        pass

    @classmethod
    @abstractmethod
    def params(cls, **kwargs) -> dict[str, str | int | float | list[str | float]]:
        pass

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def schemas(cls) -> dict[ProvidersMode, type[BaseWeatherSchema]]:
        pass

    @classmethod
    @abstractmethod
    def preprocess_data(cls, data: dict, mode: ProvidersMode) -> dict:
        pass

    @classmethod
    @abstractmethod
    async def fetch_current_weather(cls, latitude: float, longitude: float, **kwargs) -> dict:
        """Returns raw response from the weather API for current weather data."""

    @classmethod
    @abstractmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        """Returns raw response from the weather API for hourly forecast data."""
