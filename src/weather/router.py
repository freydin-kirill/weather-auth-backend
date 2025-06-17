from fastapi import APIRouter, Depends

from src.common.dependencies import get_current_active_user
from src.weather.crud import WeatherSearchDAO
from src.weather.utils import ProviderEnum, SchemaModeEnum, get_weather_adapter_by_name


router = APIRouter(
    prefix="/weather",
    tags=["Weather Service"],
)


@router.post("/current/{weather_provider}/")
async def get_weather_current(
    latitude: float,
    longitude: float,
    weather_provider: ProviderEnum,
    user=Depends(get_current_active_user),
):
    adapter = get_weather_adapter_by_name(weather_provider)
    response = await adapter.fetch_current_weather(latitude, longitude)
    await WeatherSearchDAO.log_weather_search(user.id, adapter, response)
    return adapter.get_response_schema(SchemaModeEnum.CURRENT).model_validate(response)


@router.post("/hourly_forecast/{weather_provider}/")
async def get_weather_hourly(
    latitude: float,
    longitude: float,
    weather_provider: ProviderEnum,
    user=Depends(get_current_active_user),
):
    adapter = get_weather_adapter_by_name(weather_provider)
    response = await adapter.fetch_hourly_forecast(latitude, longitude)
    await WeatherSearchDAO.log_weather_search(user.id, adapter, response)
    return adapter.get_response_schema(SchemaModeEnum.HOURLY).model_validate(response)
