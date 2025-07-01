from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request
from src.weather.models import WeatherProvider
from src.weather.schemas.base import BaseReadWeatherSchema, BaseWeatherSchema
from src.weather.schemas.meteo_source import SCurrentMeteoSourceData, SHourlyMeteoSourceData
from src.weather.utils.enums import SchemaMode


class MeteoSourceAdapter(BaseWeatherAdapter):
    @classmethod
    def schemas(cls) -> dict[SchemaMode, type[BaseWeatherSchema]]:
        return {
            SchemaMode.READ: BaseReadWeatherSchema,
            SchemaMode.CURRENT: SCurrentMeteoSourceData,
            SchemaMode.HOURLY: SHourlyMeteoSourceData,
        }

    @classmethod
    async def fetch_current_weather(
        cls, latitude: float, longitude: float, provider: WeatherProvider, **kwargs
    ) -> dict:
        params = provider.params | {
            "lat": latitude,
            "lon": longitude,
            "sections": "current",
            "key": provider.api_key,
        }
        return await send_weather_request(provider.api_url, params)

    @classmethod
    async def fetch_hourly_forecast(
        cls, latitude: float, longitude: float, provider: WeatherProvider, **kwargs
    ) -> dict:
        params = provider.params | {
            "lat": latitude,
            "lon": longitude,
            "sections": "hourly",
            "key": provider.api_key,
        }
        return await send_weather_request(provider.api_url, params)
