from src.weather.adapters.base import BaseWeatherAdapter
from src.weather.adapters.meteo_source import MeteoSourceAdapter
from src.weather.adapters.open_meteo import OpenMeteoAdapter
from src.weather.enums import Providers


def get_weather_adapter_by_name(name: Providers) -> BaseWeatherAdapter:
    providers: dict[str, BaseWeatherAdapter] = {
        Providers.OPEN_METEO.value: OpenMeteoAdapter(),
        Providers.METEO_SOURCE.value: MeteoSourceAdapter(),
    }
    try:
        return providers[name.value]
    except KeyError:
        raise ValueError(
            f"Provider '{name.value}' not found. Available providers: {', '.join(providers.keys())}"
        )


open_meteo_weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle light",
    53: "Drizzle moderate",
    55: "Drizzle dense intensity",
    56: "Freezing drizzle light",
    57: "Freezing drizzle dense intensity",
    61: "Rain slight",
    63: "Rain moderate",
    65: "Rain heavy intensity",
    66: "Freezing rain light",
    67: "Freezing rain heavy intensity",
    71: "Snow fall slight",
    73: "Snow fall moderate",
    75: "Snow fall heavy intensity",
    77: "Snow grains",
    80: "Rain showers slight",
    81: "Rain showers moderate",
    82: "Rain showers violent",
    85: "Snow showers slight",
    86: "Snow showers heavy",
    95: "Thunderstorm slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}
