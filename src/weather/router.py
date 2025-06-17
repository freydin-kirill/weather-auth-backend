from fastapi import APIRouter, Depends

from src.common.dependencies import get_current_active_user
from src.weather.crud import WeatherSearchDAO
from src.weather.providers import get_provider, get_schema_by_provider
from src.weather.utils import ProviderEnum, SchemaModeEnum


router = APIRouter(
    prefix="/weather",
    tags=["Weather Service"],
)


@router.post("/current/{weather_provider}/")
async def get_weather_current(
    latitude: float, longitude: float, weather_provider: ProviderEnum, user=Depends(get_current_active_user)
):
    provider = get_provider(weather_provider)
    response = await provider.fetch_current_weather(latitude, longitude)
    await WeatherSearchDAO.log_weather_search(user.id, weather_provider, response)
    weather_schema = get_schema_by_provider(weather_provider, SchemaModeEnum.CURRENT)
    return weather_schema.model_validate(response)


@router.post("/hourly_forecast/{weather_provider}/")
async def get_weather_hourly(
    latitude: float,
    longitude: float,
    weather_provider: ProviderEnum,
    user=Depends(get_current_active_user),
):
    provider = get_provider(weather_provider)
    response = await provider.fetch_hourly_forecast(latitude, longitude)
    await WeatherSearchDAO.log_weather_search(user.id, weather_provider, response)
    weather_schema = get_schema_by_provider(weather_provider, SchemaModeEnum.HOURLY)
    return weather_schema.model_validate(response)
