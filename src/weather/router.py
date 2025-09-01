from fastapi import APIRouter, Depends

from src.common.dependencies import get_current_active_user
from src.weather.adapters.base import preprocess_data
from src.weather.crud import ProviderDAO
from src.weather.schemas.base import BaseWeatherSchema
from src.weather.utils.enums import SchemaMode
from src.weather.utils.providers import get_weather_adapter_by_name
from src.weather.weather_fetcher.publisher import publish_weather_message


router = APIRouter(
    prefix="/weather",
    tags=["Weather Service"],
)


@router.get("/providers/", response_model=list[str])
async def get_all_weather_providers(
    user=Depends(get_current_active_user),
):
    """Return a list of available weather providers."""

    providers = await ProviderDAO.find_all(enabled=True)
    return [provider.name for provider in providers]


@router.post("/current/", response_model=dict[str, str])
async def get_all_current_weather(
    latitude: float,
    longitude: float,
    user=Depends(get_current_active_user),
):
    """Publish current weather from all enabled providers."""

    providers = await ProviderDAO.find_all(enabled=True)
    for provider in providers:
        adapter = get_weather_adapter_by_name(provider.name)
        raw_response = await adapter.fetch_current_weather(latitude, longitude, provider)
        response = preprocess_data(provider.name, raw_response, adapter.schemas().get(SchemaMode.CURRENT))
        await publish_weather_message(response)
    return {"message": "Published current weather for enabled providers"}


@router.post("/current/{weather_provider}/", response_model=dict[str, str])
async def get_current_weather(
    latitude: float,
    longitude: float,
    weather_provider: str,
    user=Depends(get_current_active_user),
):
    """Publish current weather from a specific provider."""

    provider = await ProviderDAO.find_one_or_none(name=weather_provider, enabled=True)
    if provider is None:
        raise ValueError(f"Weather provider '{weather_provider}' not found or disabled.")
    adapter = get_weather_adapter_by_name(provider.name)
    raw_response = await adapter.fetch_current_weather(latitude, longitude, provider)
    response = preprocess_data(weather_provider, raw_response, adapter.schemas().get(SchemaMode.CURRENT))
    await publish_weather_message(response)
    return {"message": f"Published current weather for provider {weather_provider}"}


@router.post("/hourly_forecast/", response_model=list[BaseWeatherSchema])
async def get_all_hourly_weather(
    latitude: float,
    longitude: float,
    user=Depends(get_current_active_user),
):
    """Return hourly forecast from all providers."""

    responses = []
    providers = await ProviderDAO.find_all(enabled=True)
    for provider in providers:
        adapter = get_weather_adapter_by_name(provider.name)
        raw_response = await adapter.fetch_hourly_forecast(latitude, longitude, provider)
        response = preprocess_data(provider.name, raw_response, adapter.schemas().get(SchemaMode.HOURLY))
        # TODO: Implement hourly forecast history saving in MongoDB
        responses.append(response)
    return responses


@router.post("/hourly_forecast/{weather_provider}/", response_model=BaseWeatherSchema)
async def get_hourly_weather(
    latitude: float,
    longitude: float,
    weather_provider: str,
    user=Depends(get_current_active_user),
):
    """Return hourly forecast from the selected provider."""

    provider = await ProviderDAO.find_one_or_none(name=weather_provider, enabled=True)
    if provider is None:
        raise ValueError(f"Weather provider '{weather_provider}' not found or disabled.")
    adapter = get_weather_adapter_by_name(provider.name)
    raw_response = await adapter.fetch_hourly_forecast(latitude, longitude, provider)
    response = preprocess_data(weather_provider, raw_response, adapter.schemas().get(SchemaMode.HOURLY))
    # TODO: Implement hourly forecast history saving in MongoDB
    return response
