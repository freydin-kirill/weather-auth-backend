from src.weather.adapters.base import BaseWeatherAdapter
from src.weather.adapters.meteo_source import MeteoSourceAdapter
from src.weather.adapters.open_meteo import OpenMeteoAdapter
from src.weather.adapters.tomorrow_io import TomorrowIOAdapter
from src.weather.utils.enums import Providers


def get_weather_adapter_by_name(name: Providers) -> BaseWeatherAdapter:
    providers: dict[str, BaseWeatherAdapter] = {
        Providers.OPEN_METEO.value: OpenMeteoAdapter(),
        Providers.METEO_SOURCE.value: MeteoSourceAdapter(),
        Providers.TOMORROW_IO.value: TomorrowIOAdapter(),
    }
    try:
        return providers[name.value]
    except KeyError:
        raise ValueError(
            f"Provider '{name.value}' not found. Available providers: {', '.join(providers.keys())}"
        )
