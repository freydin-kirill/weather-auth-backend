from fastapi import APIRouter, Depends

from src.common.dependencies import get_current_active_user
from src.weather.crud import CurrentWeatherDAO
from src.weather.schemas.base import BaseWeatherSchema
from src.weather.utils.enums import Providers, SchemaMode
from src.weather.utils.providers import get_weather_adapter_by_name


router = APIRouter(
    prefix="/weather",
    tags=["Weather Service"],
)


@router.post("/current/", response_model=list[BaseWeatherSchema])
async def get_all_current_weather(
    latitude: float,
    longitude: float,
    user=Depends(get_current_active_user),
):
    responses = []
    for provider in Providers:
        adapter = get_weather_adapter_by_name(provider)
        raw_response = await adapter.fetch_current_weather(latitude, longitude)
        response = adapter.preprocess_data(raw_response, SchemaMode.CURRENT)
        await CurrentWeatherDAO.create(**response)
        responses.append(response)
    return responses


@router.post("/current/{weather_provider}/", response_model=BaseWeatherSchema)
async def get_current_weather(
    latitude: float,
    longitude: float,
    weather_provider: Providers,
    user=Depends(get_current_active_user),
):
    adapter = get_weather_adapter_by_name(weather_provider)
    raw_response = await adapter.fetch_current_weather(latitude, longitude)
    response = adapter.preprocess_data(raw_response, SchemaMode.CURRENT)
    await CurrentWeatherDAO.create(**response)
    return response


@router.post("/hourly_forecast/", response_model=list[BaseWeatherSchema])
async def get_all_hourly_weather(
    latitude: float,
    longitude: float,
    user=Depends(get_current_active_user),
):
    responses = []
    for provider in Providers:
        adapter = get_weather_adapter_by_name(provider)
        raw_response = await adapter.fetch_hourly_forecast(latitude, longitude)
        response = adapter.preprocess_data(raw_response, SchemaMode.HOURLY)
        # TODO: Implement hourly forecast history saving in MongoDB
        responses.append(response)
    return responses


@router.post("/hourly_forecast/{weather_provider}/", response_model=BaseWeatherSchema)
async def get_hourly_weather(
    latitude: float,
    longitude: float,
    weather_provider: Providers,
    user=Depends(get_current_active_user),
):
    adapter = get_weather_adapter_by_name(weather_provider)
    raw_response = await adapter.fetch_hourly_forecast(latitude, longitude)
    response = adapter.preprocess_data(raw_response, SchemaMode.HOURLY)
    # TODO: Implement hourly forecast history saving in MongoDB
    return response
