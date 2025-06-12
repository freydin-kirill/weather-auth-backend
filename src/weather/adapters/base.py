from abc import ABC, abstractmethod

from httpx import AsyncClient


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
    async def fetch_current_weather(cls, latitude: float, longitude: float, **kwargs) -> dict:
        pass

    @classmethod
    @abstractmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        pass
