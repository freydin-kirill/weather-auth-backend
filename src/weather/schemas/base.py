from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field


class BaseWeatherSchema(BaseModel):
    timezone: str
    latitude: float | str = Field(validation_alias=AliasChoices("lat", "latitude"))
    longitude: float | str = Field(validation_alias=AliasChoices("lon", "longitude"))


class BaseWriteWeatherSchema(BaseModel):
    user_id: int
    provider: str


class BaseReadWeatherSchema(BaseModel):
    id: int
    created_at: datetime
