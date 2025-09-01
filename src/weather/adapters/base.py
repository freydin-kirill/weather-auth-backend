from abc import ABC, abstractmethod

from httpx import AsyncClient

from src.weather.models import WeatherProvider
from src.weather.schemas.base import BaseWeatherSchema
from src.weather.utils.enums import SchemaMode


async def send_weather_request(url: str, params: dict) -> dict:
    """Send a GET request to a weather API.

    :param url: service URL, str
    :param params: request parameters, dict
    :returns: service response as dictionary, dict
    """

    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


def preprocess_data(name: str, data: dict, schema: BaseWeatherSchema | None) -> dict:
    """Validate and enrich provider data with schema."""

    if not schema:
        raise ValueError(f"Schema for {name} not found.")
    data.update({"provider": name})
    return schema.model_validate(data).model_dump()


class BaseWeatherAdapter(ABC):
    """Base class for weather service adapters."""

    @classmethod
    @abstractmethod
    def schemas(cls) -> dict[SchemaMode, type[BaseWeatherSchema]]:
        """Return data schemas for different modes."""

        pass

    @classmethod
    @abstractmethod
    async def fetch_current_weather(
        cls, latitude: float, longitude: float, provider: WeatherProvider, **kwargs
    ) -> dict:
        """Fetch current weather from the service."""

    @classmethod
    @abstractmethod
    async def fetch_hourly_forecast(
        cls, latitude: float, longitude: float, provider: WeatherProvider, **kwargs
    ) -> dict:
        """Fetch hourly forecast from the service."""
