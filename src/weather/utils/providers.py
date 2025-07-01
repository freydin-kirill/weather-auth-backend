from src.weather.adapters.base import BaseWeatherAdapter
from src.weather.adapters.meteo_source import MeteoSourceAdapter
from src.weather.adapters.open_meteo import OpenMeteoAdapter


def get_weather_adapter_by_name(name: str) -> BaseWeatherAdapter:
    providers: dict[str, BaseWeatherAdapter] = {
        "open_meteo": OpenMeteoAdapter(),
        "meteo_source": MeteoSourceAdapter(),
    }
    try:
        return providers[name]
    except KeyError:
        raise ValueError(f"Provider '{name}' not found. Available providers: {', '.join(providers.keys())}")
