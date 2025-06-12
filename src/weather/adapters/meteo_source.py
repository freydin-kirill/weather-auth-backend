from src.config import settings
from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request


class MeteoSourceAdapter(BaseWeatherAdapter):
    _url: str = settings.METEO_SOURCE_API_URL
    _params: dict[str, str | float | int | list[str]] = {
        "lat": 0.0,
        "lon": 0.0,
        "timezone": "auto",
        "key": settings.METEO_SOURCE_API_KEY,
    }

    @classmethod
    async def fetch_current_weather(cls, latitude: float, longitude: float, **kwargs) -> dict:
        cls._params.update(
            {
                "lat": latitude,
                "lon": longitude,
                "sections": "current",
            }
        )
        return await send_weather_request(cls._url, cls._params)

    @classmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        cls._params.update(
            {
                "lat": latitude,
                "lon": longitude,
                "sections": "hourly",
            }
        )
        return await send_weather_request(cls._url, cls._params)
