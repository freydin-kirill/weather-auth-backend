from fastapi import APIRouter, Depends

from src.common.dependencies import get_current_active_user
from src.weather.utils.enums import Providers, SchemaMode
from src.weather.utils.providers import get_weather_adapter_by_name


router = APIRouter(
    prefix="/weather",
    tags=["Weather Service"],
)


@router.post("/current/{weather_provider}/")
async def get_weather_current(
    latitude: float,
    longitude: float,
    weather_provider: Providers,
    user=Depends(get_current_active_user),
):
    adapter = get_weather_adapter_by_name(weather_provider)
    response = await adapter.fetch_current_weather(latitude, longitude)
    return adapter.get_response_schema(SchemaMode.CURRENT).model_validate(response)


@router.post("/hourly_forecast/{weather_provider}/")
async def get_weather_hourly(
    latitude: float,
    longitude: float,
    weather_provider: Providers,
    user=Depends(get_current_active_user),
):
    adapter = get_weather_adapter_by_name(weather_provider)
    response = await adapter.fetch_hourly_forecast(latitude, longitude)
    return adapter.get_response_schema(SchemaMode.HOURLY).model_validate(response)
