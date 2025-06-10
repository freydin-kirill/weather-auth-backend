from httpx import AsyncClient

from src.config import settings


async def send_weather_request(params: dict) -> dict:
    async with AsyncClient() as client:
        response = await client.get(settings.WEATHER_API_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


async def fetch_current_weather(
    latitude: list[float],
    longitude: list[float],
) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "auto",
        "current": [
            "temperature_2m",
            "weather_code",
            "relative_humidity_2m",
            "pressure_msl",
        ],
    }

    return await send_weather_request(params)


async def fetch_forecast_weather(
    days: int,
    latitude: list[float],
    longitude: list[float],
) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "auto",
        "hourly": [
            "temperature_2m",
            "weather_code",
            "relative_humidity_2m",
            "pressure_msl",
        ],
        "forecast_days": days,
    }

    return await send_weather_request(params)
