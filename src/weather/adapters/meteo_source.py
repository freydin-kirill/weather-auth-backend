from src.config import settings
from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request
from src.weather.schemas.base import BaseReadWeatherSchema, BaseWeatherSchema
from src.weather.schemas.meteo_source import SCurrentMeteoSourceData, SHourlyMeteoSourceData
from src.weather.utils.enums import Providers, ProvidersMode


class MeteoSourceAdapter(BaseWeatherAdapter):
    @classmethod
    def url(cls, **kwargs) -> str:
        return settings.METEO_SOURCE_API_URL

    @classmethod
    def params(cls, **kwargs) -> dict[str, str | int | float | list[str | float]]:
        return {
            "lat": 0.0,
            "lon": 0.0,
            "timezone": "auto",
            "key": settings.METEO_SOURCE_API_KEY,
        }

    @classmethod
    def name(cls) -> str:
        return Providers.METEO_SOURCE.value

    @classmethod
    def schemas(cls) -> dict[ProvidersMode, type[BaseWeatherSchema]]:
        return {
            ProvidersMode.READ: BaseReadWeatherSchema,
            ProvidersMode.CURRENT: SCurrentMeteoSourceData,
            ProvidersMode.HOURLY: SHourlyMeteoSourceData,
        }

    @classmethod
    def preprocess_data(cls, data: dict, mode: ProvidersMode) -> dict:
        data.update({"provider": cls.name()})
        schema = cls.schemas().get(mode, None)
        if not schema:
            raise ValueError(f"Schema for mode {mode} not found in {cls.name()} adapter.")
        return schema.model_validate(data).model_dump()

    @classmethod
    async def fetch_current_weather(cls, latitude: float, longitude: float, **kwargs) -> dict:
        params = cls.params() | {
            "lat": latitude,
            "lon": longitude,
            "sections": "current",
        }
        return await send_weather_request(cls.url(), params)

    @classmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        params = cls.params() | {
            "lat": latitude,
            "lon": longitude,
            "sections": "hourly",
        }
        return await send_weather_request(cls.url(), params)
