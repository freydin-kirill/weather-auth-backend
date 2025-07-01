from src.common.crud import BaseDAO
from src.weather.models import CurrentWeatherHistory, WeatherProvider


class CurrentWeatherDAO(BaseDAO[CurrentWeatherHistory]):
    """
    Data Access Object (DAO) for weather history-related operations.
    This class provides methods to interact with the database for weather history management.
    """

    model = CurrentWeatherHistory


class ProviderDAO(BaseDAO[WeatherProvider]):
    """
    Data Access Object (DAO) for weather provider-related operations.
    This class provides methods to interact with the database for weather provider management.
    """

    model = WeatherProvider
