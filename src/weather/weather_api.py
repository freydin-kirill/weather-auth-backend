from httpx import AsyncClient

from src.config import settings


class WeatherAPI:
    _base_url = settings.WEATHER_API_BASE_URL
    _params: dict[str, str | int | list[str | float]] = {
        "latitude": None,
        "longitude": None,
        "timezone": "auto",
    }

    @classmethod
    async def send_weather_request(cls) -> dict:
        async with AsyncClient() as client:
            response = await client.get(cls._base_url, params=cls._params)
            response.raise_for_status()
            return response.json()

    @classmethod
    async def fetch_current_weather(cls, latitude: list[float], longitude: list[float]) -> dict:
        cls._params.update({"latitude": latitude, "longitude": longitude})
        cls._params["current"] = [
            "temperature_2m",
            "weather_code",
            "relative_humidity_2m",
            "pressure_msl",
        ]

        return await cls.send_weather_request()

    @classmethod
    async def fetch_forecast_weather(cls, days: int, latitude: list[float], longitude: list[float]) -> dict:
        cls._params.update({"latitude": latitude, "longitude": longitude, "days": days})
        cls._params["hourly"] = [
            "temperature_2m",
            "weather_code",
            "relative_humidity_2m",
            "pressure_msl",
        ]

        return await cls.send_weather_request()
