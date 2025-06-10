from fastapi import APIRouter, Body

from src.weather.schemas import SCurrentWeatherData, SForecastWeatherData
from src.weather.weather_api import fetch_current_weather, fetch_forecast_weather


router = APIRouter(
    prefix="/weather",
    tags=["Weather Service"],
)


@router.post("/now/", response_model=SCurrentWeatherData)
async def get_weather_current(latitude: list[float], longitude: list[float]):
    response = await fetch_current_weather(latitude, longitude)
    return SCurrentWeatherData.model_validate(response)


@router.post("/forecast/", response_model=SForecastWeatherData)
async def get_weather_forecast(
    days: int = Body(),
    latitude: list[float] = Body(),
    longitude: list[float] = Body(),
):
    response = await fetch_forecast_weather(days, latitude, longitude)
    return SForecastWeatherData.model_validate(response)
