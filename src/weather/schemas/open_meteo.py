from pydantic import AliasGenerator, AliasPath, ConfigDict, field_validator

from src.weather.schemas.base import BaseWeatherSchema
from src.weather.utils.open_meteo import open_meteo_weather_codes


_ALIAS_MAP = {
    "time": "time",
    "summary": "weather_code",
    "temperature": "temperature_2m",
    "wind_speed": "wind_speed_10m",
}


def _make_aliases(path: str, field_name: str) -> AliasPath | None:
    if field_name in _ALIAS_MAP:
        return AliasPath(path, _ALIAS_MAP[field_name])
    return None


class SCurrentOpenMeteoData(BaseWeatherSchema):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: _make_aliases("current", field_name),
        )
    )

    @field_validator("summary", mode="before")
    @classmethod
    def _validate_weather_code(cls, value: int) -> str:
        return open_meteo_weather_codes.get(value, "Unknown")


class SHourlyOpenMeteoData(BaseWeatherSchema):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: _make_aliases("hourly", field_name),
        )
    )

    @field_validator("summary", mode="before")
    @classmethod
    def _validate_weather_codes(cls, values: list[int]) -> list[str]:
        return [open_meteo_weather_codes.get(code, "Unknown") for code in values]
