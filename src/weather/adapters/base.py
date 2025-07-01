from abc import ABC, abstractmethod

from httpx import AsyncClient

from src.weather.models import WeatherProvider
from src.weather.schemas.base import BaseWeatherSchema
from src.weather.utils.enums import SchemaMode


async def send_weather_request(url, params) -> dict:
    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


def preprocess_data(name: str, data: dict, schema: BaseWeatherSchema | None) -> dict:
    if not schema:
        raise ValueError(f"Schema for {name} not found.")
    data.update({"provider": name})
    return schema.model_validate(data).model_dump()


class BaseWeatherAdapter(ABC):
    """Base class for weather adapters."""

    @classmethod
    @abstractmethod
    def schemas(cls) -> dict[SchemaMode, type[BaseWeatherSchema]]:
        pass

    @classmethod
    @abstractmethod
    async def fetch_current_weather(
        cls, latitude: float, longitude: float, provider: WeatherProvider, **kwargs
    ) -> dict:
        """Returns raw response from the weather API for current weather data."""

    @classmethod
    @abstractmethod
    async def fetch_hourly_forecast(
        cls, latitude: float, longitude: float, provider: WeatherProvider, **kwargs
    ) -> dict:
        """Returns raw response from the weather API for hourly forecast data."""
