from datetime import datetime

from pydantic import AliasPath, BaseModel, Field


class SBaseWeatherData(BaseModel):
    latitude: float
    longitude: float
    timezone: str


# noinspection PyTypeChecker
class SCurrentWeatherData(SBaseWeatherData):
    current_time: datetime = Field(alias=AliasPath("current", "time"))
    current_temperature: float = Field(alias=AliasPath("current", "temperature_2m"))
    current_weather: int = Field(default=None, alias=AliasPath("current", "weather_code"))
    current_humidity: int = Field(default=None, alias=AliasPath("current", "relative_humidity_2m"))
    current_pressure: float = Field(default=None, alias=AliasPath("current", "pressure_msl"))


# noinspection PyTypeChecker
class SForecastWeatherData(SBaseWeatherData):
    forcast_time: list[datetime] = Field(alias=AliasPath("hourly", "time"))
    forcast_temperature: list[float] = Field(alias=AliasPath("hourly", "temperature_2m"))

    forcast_weather: list[int] | None = Field(default=None, alias=AliasPath("hourly", "weather_code"))
    forcast_humidity: list[float] | None = Field(default=None, alias=AliasPath("hourly", "relative_humidity_2m"))
    forcast_pressure: list[float] | None = Field(default=None, alias=AliasPath("hourly", "pressure_msl"))
