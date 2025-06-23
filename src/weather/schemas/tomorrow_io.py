from datetime import datetime
from typing import Any

from pydantic import AliasPath, Field, model_validator

from src.weather.schemas.base import BaseWeatherSchema
from src.weather.utils.tomorrow_io import tomorrow_io_weather_codes


class SBaseTomorrowIOData(BaseWeatherSchema):
    latitude: float = Field(validation_alias=AliasPath("location", "lat"))
    longitude: float = Field(validation_alias=AliasPath("location", "lon"))


class SCurrentTomorrowIOData(SBaseTomorrowIOData):
    time: datetime = Field(validation_alias=AliasPath("data", "time"))

    @model_validator(mode="before")
    @classmethod
    def _flatten_data(cls, values: dict[str, Any]):
        current_data = values.get("data", {}).get("values", {})
        values["wind_speed"] = current_data.get("windSpeed", 0.0)
        values["summary"] = tomorrow_io_weather_codes.get(current_data.get("weatherCode", 0))
        values["temperature"] = current_data.get("temperature", 0.0)

        return values


class SHourlyTomorrowIOData(SBaseTomorrowIOData):
    @model_validator(mode="before")
    @classmethod
    def _flatten_data(cls, values: dict[str, Any]):
        hourly_data = values.get("timelines", {}).get("hourly", {})

        times: list[datetime] = []
        summaries: list[str] = []
        temperatures: list[float] = []
        winds: list[float] = []

        for item in hourly_data:
            times.append(item.get("time"))
            item_values = item.get("values", {})
            temperatures.append(item_values.get("temperature", 0.0))
            summaries.append(tomorrow_io_weather_codes.get(item_values.get("weatherCode", 0)))
            winds.append(item_values.get("windSpeed", 0.0))

        values["time"] = times
        values["wind_speed"] = winds
        values["summary"] = summaries
        values["temperature"] = temperatures

        return values
