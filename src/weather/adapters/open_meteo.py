from src.config import settings
from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request
from src.weather.schemas.base import BaseReadWeatherSchema, BaseWeatherSchema
from src.weather.schemas.open_meteo import SCurrentOpenMeteoData, SHourlyOpenMeteoData
from src.weather.utils.enums import Providers, ProvidersMode


class OpenMeteoAdapter(BaseWeatherAdapter):
    _fields: list[str] = [
        "temperature_2m",
        "weather_code",
        "wind_speed_10m",
    ]

    @classmethod
    def url(cls, **kwargs) -> str:
        return settings.OPEN_METEO_API_URL

    @classmethod
    def params(cls, **kwargs) -> dict[str, str | int | float | list[str | float]]:
        return {
            "latitude": 0.0,
            "longitude": 0.0,
            "timezone": "auto",
        }

    @classmethod
    def name(cls) -> str:
        return Providers.OPEN_METEO.value

    @classmethod
    def schemas(cls) -> dict[ProvidersMode, type[BaseWeatherSchema]]:
        return {
            ProvidersMode.READ: BaseReadWeatherSchema,
            ProvidersMode.CURRENT: SCurrentOpenMeteoData,
            ProvidersMode.HOURLY: SHourlyOpenMeteoData,
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
            "latitude": latitude,
            "longitude": longitude,
            "current": cls._fields,
        }
        return await send_weather_request(cls.url(), params)

    @classmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        params = cls.params() | {
            "latitude": latitude,
            "longitude": longitude,
            "days": kwargs.get("days", 1),
            "hourly": cls._fields,
        }
        return await send_weather_request(cls.url(), params)
