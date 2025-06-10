from fastapi import APIRouter, Body, Depends

from src.common.dependencies import get_current_active_user
from src.weather.schemas import SCurrentWeatherData, SForecastWeatherData
from src.weather.weather_api import WeatherAPI


router = APIRouter(
    prefix="/weather",
    tags=["Weather Service"],
)


@router.post("/current/", response_model=SCurrentWeatherData)
async def get_weather_current(latitude: list[float], longitude: list[float], user=Depends(get_current_active_user)):
    response = await WeatherAPI.fetch_current_weather(latitude, longitude)
    return SCurrentWeatherData.model_validate(response)


@router.post("/forecast/", response_model=SForecastWeatherData)
async def get_weather_forecast(
    days: int = Body(),
    latitude: list[float] = Body(),
    longitude: list[float] = Body(),
    user=Depends(get_current_active_user),
):
    response = await WeatherAPI.fetch_forecast_weather(days, latitude, longitude)
    return SForecastWeatherData.model_validate(response)
