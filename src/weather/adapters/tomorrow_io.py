from src.config import settings
from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request
from src.weather.schemas.base import BaseReadWeatherSchema, BaseWeatherSchema
from src.weather.schemas.tomorrow_io import SCurrentTomorrowIOData, SHourlyTomorrowIOData
from src.weather.utils.enums import Providers, ProvidersMode


class TomorrowIOAdapter(BaseWeatherAdapter):
    @classmethod
    def url(cls, **kwargs) -> str:
        mode = kwargs.get("mode", ProvidersMode.CURRENT)
        if mode == ProvidersMode.HOURLY:
            return settings.TOMORROW_IO_HOURLY_API_URL
        return settings.TOMORROW_IO_CURRENT_API_URL

    @classmethod
    def params(cls, **kwargs) -> dict[str, str | int | float | list[str | float]]:
        return {
            "location": f"{0.0},{0.0}",
            "apikey": settings.TOMORROW_IO_API_KEY,
        }

    @classmethod
    def name(cls) -> str:
        return Providers.TOMORROW_IO.value

    @classmethod
    def schemas(cls) -> dict[ProvidersMode, type[BaseWeatherSchema]]:
        return {
            ProvidersMode.READ: BaseReadWeatherSchema,
            ProvidersMode.CURRENT: SCurrentTomorrowIOData,
            ProvidersMode.HOURLY: SHourlyTomorrowIOData,
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
            "location": f"{latitude},{longitude}",
        }
        return await send_weather_request(cls.url(mode=ProvidersMode.CURRENT), params)

    @classmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        params = cls.params() | {
            "location": f"{latitude},{longitude}",
            "timesteps": "1h",
        }
        return await send_weather_request(cls.url(mode=ProvidersMode.HOURLY), params)
