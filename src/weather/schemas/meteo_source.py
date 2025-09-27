from datetime import datetime
from typing import Any

from pydantic import AliasPath, Field, model_validator

from src.weather.schemas.base import BaseWeatherSchema


class SCurrentMeteoSourceData(BaseWeatherSchema):
    """Schema for current weather from MeteoSource."""

    summary: str = Field(validation_alias=AliasPath("current", "summary"))
    temperature: float = Field(validation_alias=AliasPath("current", "temperature"))
    wind_speed: float = Field(validation_alias=AliasPath("current", "wind", "speed"))

    @model_validator(mode="before")
    @classmethod
    def _ensure_time(cls, values: dict[str, Any]):
        """Add current timestamp."""

        values["time"] = datetime.now()
        return values


class SHourlyMeteoSourceData(BaseWeatherSchema):
    """Schema for hourly forecast from MeteoSource."""

    @model_validator(mode="before")
    @classmethod
    def _flatten_data(cls, values: dict[str, Any]):
        """Flatten nested data into a simple format."""

        hourly_data = values.get("hourly", {}).get("data", {})

        times: list[datetime] = []
        summaries: list[str] = []
        temperatures: list[float] = []
        winds: list[float] = []

        for item in hourly_data:
            times.append(item.get("date"))
            temperatures.append(item.get("temperature", 0.0))
            summaries.append(item.get("summary", ""))
            winds.append(item.get("wind", {}).get("speed", 0.0))

        values["time"] = times
        values["wind_speed"] = winds
        values["summary"] = summaries
        values["temperature"] = temperatures

        return values
