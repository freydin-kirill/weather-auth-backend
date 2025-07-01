from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request
from src.weather.models import WeatherProvider
from src.weather.schemas.base import BaseReadWeatherSchema, BaseWeatherSchema
from src.weather.schemas.open_meteo import SCurrentOpenMeteoData, SHourlyOpenMeteoData
from src.weather.utils.enums import SchemaMode


class OpenMeteoAdapter(BaseWeatherAdapter):
    _fields: list[str] = [
        "temperature_2m",
        "weather_code",
        "wind_speed_10m",
    ]

    @classmethod
    def schemas(cls) -> dict[SchemaMode, type[BaseWeatherSchema]]:
        return {
            SchemaMode.READ: BaseReadWeatherSchema,
            SchemaMode.CURRENT: SCurrentOpenMeteoData,
            SchemaMode.HOURLY: SHourlyOpenMeteoData,
        }

    @classmethod
    async def fetch_current_weather(
        cls, latitude: float, longitude: float, provider: WeatherProvider, **kwargs
    ) -> dict:
        params = provider.params | {
            "timezone": "auto",
            "latitude": latitude,
            "longitude": longitude,
            "current": cls._fields,
        }
        return await send_weather_request(provider.api_url, params)

    @classmethod
    async def fetch_hourly_forecast(
        cls, latitude: float, longitude: float, provider: WeatherProvider, **kwargs
    ) -> dict:
        params = provider.params | {
            "timezone": "auto",
            "latitude": latitude,
            "longitude": longitude,
            "days": kwargs.get("days", 1),
            "hourly": cls._fields,
        }
        return await send_weather_request(provider.api_url, params)
