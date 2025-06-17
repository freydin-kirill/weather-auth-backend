from datetime import datetime
from typing import Any

from pydantic import AliasChoices, AliasPath, Field, field_validator

from src.weather.schemas.base import BaseReadWeatherSchema, BaseWeatherSchema, BaseWriteWeatherSchema
from src.weather.utils import open_meteo_weather_codes


class SCurrentOpenMeteoData(BaseWeatherSchema):
    time: datetime = Field(validation_alias=AliasPath("current", "time"))
    temperature: float = Field(validation_alias=AliasPath("current", "temperature_2m"))
    weather: str | int = Field(default=None, validation_alias=AliasPath("current", "weather_code"))
    wind_speed: float = Field(validation_alias=AliasPath("current", "wind_speed_10m"))

    @field_validator("weather", mode="before")
    @classmethod
    def _validate_weather_code(cls, value: int) -> str:
        return open_meteo_weather_codes.get(value, "Unknown")


class SHourlyOpenMeteoData(BaseWeatherSchema):
    time: list[datetime] = Field(validation_alias=AliasPath("hourly", "time"))
    temperature: list[float] = Field(validation_alias=AliasPath("hourly", "temperature_2m"))
    weather: list[str | int] = Field(default=None, validation_alias=AliasPath("hourly", "weather_code"))
    wind_speed: list[float] = Field(validation_alias=AliasPath("hourly", "wind_speed_10m"))

    @field_validator("weather", mode="before")
    @classmethod
    def _validate_weather_codes(cls, values: list[int]) -> list[str]:
        return [open_meteo_weather_codes.get(code, "Unknown") for code in values]


class SWriteOpenMeteoData(BaseWriteWeatherSchema):
    data: dict[str, Any] = Field(validation_alias=AliasChoices("current", "hourly"))


class SReadOpenMeteoData(BaseReadWeatherSchema, SWriteOpenMeteoData):
    pass
