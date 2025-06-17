from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import AliasPath, Field, model_validator

from src.weather.schemas.base import BaseReadWeatherSchema, BaseWeatherSchema, BaseWriteWeatherSchema


class SCurrentMeteoSourceData(BaseWeatherSchema):
    time: datetime
    temperature: float = Field(validation_alias=AliasPath("current", "temperature"))
    weather: str = Field(default=None, validation_alias=AliasPath("current", "summary"))
    wind_speed: float = Field(validation_alias=AliasPath("current", "wind", "speed"))

    @model_validator(mode="before")
    @classmethod
    def _ensure_time(cls, values: dict[str, Any]):
        values["time"] = datetime.now(ZoneInfo(values.get("timezone")))
        return values


class SHourlyMeteoSourceData(BaseWeatherSchema):
    time: list[datetime]
    temperature: list[float]
    weather: list[str]
    wind_speed: list[float]

    @model_validator(mode="before")
    @classmethod
    def _flatten_data(cls, values: dict[str, Any]):
        hourly_data = values.get("hourly", {}).get("data", {})

        times: list[datetime] = []
        temps: list[float] = []
        weathers: list[str] = []
        winds: list[float] = []

        for item in hourly_data:
            times.append(item.get("date"))
            temps.append(item.get("temperature", 0.0))
            weathers.append(item.get("summary", ""))
            winds.append(item.get("wind", {}).get("speed", 0.0))

        values["time"] = times
        values["temperature"] = temps
        values["weather"] = weathers
        values["wind_speed"] = winds

        return values


class SWriteMeteoSourceData(BaseWriteWeatherSchema):
    data: dict[str, Any] = Field(...)

    @model_validator(mode="before")
    @classmethod
    def _create_write_data(cls, values: dict[str, Any]):
        data: dict[str, Any] = {}
        if values.get("current") is not None:
            data = values.get("current")
        elif values.get("hourly") is not None:
            data = values.get("hourly")

        values["data"] = data

        return values


class SReadMeteoSourceData(BaseReadWeatherSchema, SWriteMeteoSourceData):
    pass
