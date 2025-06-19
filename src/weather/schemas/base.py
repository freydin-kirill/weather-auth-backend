import re

from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field, field_validator


class BaseWeatherSchema(BaseModel):
    timezone: str
    latitude: float = Field(validation_alias=AliasChoices("lat", "latitude"))
    longitude: float = Field(validation_alias=AliasChoices("lon", "longitude"))

    provider: str
    summary: str | list[str]
    temperature: float | list[float]
    wind_speed: float | list[float]
    time: datetime | list[datetime]

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def _ensure_coordinates(cls, value: float | str) -> float:
        if isinstance(value, str):
            value = float(re.findall(r"(\d+\.?\d*)", value)[0])
        return value


class BaseReadWeatherSchema(BaseWeatherSchema):
    id: int
    created_at: datetime
