from enum import Enum

from src.weather.adapters.base import BaseWeatherAdapter
from src.weather.adapters.meteo_source import MeteoSourceAdapter
from src.weather.adapters.open_meteo import OpenMeteoAdapter


class ProviderEnum(Enum):
    OPEN_METEO = "open_meteo"
    METEO_SOURCE = "meteo_source"


def get_provider(name: str) -> BaseWeatherAdapter:
    providers: dict[str, BaseWeatherAdapter] = {
        ProviderEnum.OPEN_METEO.value: OpenMeteoAdapter(),
        ProviderEnum.METEO_SOURCE.value: MeteoSourceAdapter(),
    }
    try:
        return providers[name]
    except KeyError:
        raise ValueError(f"Provider '{name}' not found. Available providers: {', '.join(providers.keys())}")
