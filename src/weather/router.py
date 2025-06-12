from fastapi import APIRouter, Depends

from src.common.dependencies import get_current_active_user
from src.weather.providers import ProviderEnum, get_provider
from src.weather.schemas import CurrentWeatherSchema, HourlyWeatherSchema


router = APIRouter(
    prefix="/weather",
    tags=["Weather Service"],
)


@router.post("/current/{weather_provider}/", response_model=CurrentWeatherSchema)
async def get_weather_current(
    latitude: float, longitude: float, weather_provider: ProviderEnum, user=Depends(get_current_active_user)
):
    provider = get_provider(weather_provider.value)
    response = await provider.fetch_current_weather(latitude, longitude)
    return CurrentWeatherSchema.model_validate(response)


@router.post("/hourly_forecast/{weather_provider}/", response_model=HourlyWeatherSchema)
async def get_weather_hourly(
    latitude: float,
    longitude: float,
    weather_provider: ProviderEnum,
    user=Depends(get_current_active_user),
):
    provider = get_provider(weather_provider.value)
    response = await provider.fetch_hourly_forecast(latitude, longitude)
    return HourlyWeatherSchema.model_validate(response)
