from src.config import settings
from src.weather.adapters.base import BaseWeatherAdapter, send_weather_request
from src.weather.schemas.base import BaseWeatherSchema, BaseWriteWeatherSchema
from src.weather.schemas.open_meteo import SCurrentOpenMeteoData, SHourlyOpenMeteoData, SWriteOpenMeteoData
from src.weather.utils import ProviderEnum, SchemaModeEnum


class OpenMeteoAdapter(BaseWeatherAdapter):
    _url: str = settings.OPEN_METEO_API_URL
    _params: dict[str, str | float | int | list[str]] = {
        "latitude": 0.0,
        "longitude": 0.0,
        "timezone": "auto",
    }

    @classmethod
    def name(cls) -> str:
        return ProviderEnum.OPEN_METEO.value

    @classmethod
    def get_write_schema(cls) -> type[BaseWriteWeatherSchema]:
        return SWriteOpenMeteoData

    @classmethod
    def get_response_schema(cls, mode: SchemaModeEnum) -> type[BaseWeatherSchema]:
        schemas = {
            SchemaModeEnum.CURRENT.value: SCurrentOpenMeteoData,
            SchemaModeEnum.HOURLY.value: SHourlyOpenMeteoData,
        }
        return schemas[mode.value]

    @classmethod
    async def fetch_current_weather(cls, latitude: float, longitude: float, **kwargs) -> dict:
        cls._params.update({"latitude": latitude, "longitude": longitude})
        cls._params["current"] = [
            "temperature_2m",
            "weather_code",
            "wind_speed_10m",
        ]
        return await send_weather_request(cls._url, cls._params)

    @classmethod
    async def fetch_hourly_forecast(cls, latitude: float, longitude: float, **kwargs) -> dict:
        cls._params.update({"latitude": latitude, "longitude": longitude, "days": kwargs.get("days", 1)})
        cls._params["hourly"] = [
            "temperature_2m",
            "weather_code",
            "wind_speed_10m",
        ]
        return await send_weather_request(cls._url, cls._params)
