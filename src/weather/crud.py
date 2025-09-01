from src.common.crud import BaseDAO
from src.weather.models import CurrentWeatherHistory, WeatherProvider


class CurrentWeatherDAO(BaseDAO[CurrentWeatherHistory]):
    """DAO for working with current weather history."""

    model = CurrentWeatherHistory


class ProviderDAO(BaseDAO[WeatherProvider]):
    """DAO for managing weather providers."""

    model = WeatherProvider
