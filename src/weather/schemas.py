from typing import Any

from pydantic import AliasChoices, BaseModel, Field


class BaseWeatherSchema(BaseModel):
    timezone: str
    latitude: float | str = Field(validation_alias=AliasChoices("lat", "latitude"))
    longitude: float | str = Field(validation_alias=AliasChoices("lon", "longitude"))


class CurrentWeatherSchema(BaseWeatherSchema):
    current: dict[str, Any] | None


class HourlyWeatherSchema(BaseWeatherSchema):
    hourly: dict[str, Any] | None
