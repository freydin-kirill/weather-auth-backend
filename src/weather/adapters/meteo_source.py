from src.config import settings
from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request
from src.weather.enums import Providers, SchemaMode
from src.weather.schemas.base import BaseWeatherSchema, BaseWriteWeatherSchema
from src.weather.schemas.meteo_source import (
    SCurrentMeteoSourceData,
    SHourlyMeteoSourceData,
    SWriteMeteoSourceData,
)


class MeteoSourceAdapter(BaseWeatherAdapter):
    _url: str = settings.METEO_SOURCE_API_URL
    _params: dict[str, str | float | int | list[str]] = {
        "lat": 0.0,
        "lon": 0.0,
        "timezone": "auto",
        "key": settings.METEO_SOURCE_API_KEY,
    }

    @classmethod
    def name(cls) -> str:
        return Providers.METEO_SOURCE.value

    @classmethod
    def get_write_schema(cls) -> type[BaseWriteWeatherSchema]:
        return SWriteMeteoSourceData

    @classmethod
    def get_response_schema(cls, mode: SchemaMode) -> type[BaseWeatherSchema]:
        schemas = {
            SchemaMode.CURRENT.value: SCurrentMeteoSourceData,
            SchemaMode.HOURLY.value: SHourlyMeteoSourceData,
        }
        return schemas[mode.value]

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
