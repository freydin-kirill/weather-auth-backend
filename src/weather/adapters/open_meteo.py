from src.config import settings
from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request


class OpenMeteoAdapter(BaseWeatherAdapter):
    _url: str = settings.OPEN_METEO_API_URL
    _params: dict[str, str | float | int | list[str]] = {
        "latitude": 0.0,
        "longitude": 0.0,
        "timezone": "auto",
    }

    @classmethod
    async def fetch_current_weather(cls, latitude: float, longitude: float, **kwargs) -> dict:
        cls._params.update({"latitude": latitude, "longitude": longitude})
        cls._params["current"] = [
            "temperature_2m",
            "weather_code",
            "relative_humidity_2m",
            "pressure_msl",
        ]
        return await send_weather_request(cls._url, cls._params)

    @classmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        cls._params.update({"latitude": latitude, "longitude": longitude, "days": kwargs.get("days", 1)})
        cls._params["hourly"] = [
            "temperature_2m",
            "weather_code",
            "relative_humidity_2m",
            "pressure_msl",
        ]
        return await send_weather_request(cls._url, cls._params)
