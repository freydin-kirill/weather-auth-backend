from src.common.crud import BaseDAO
from src.weather.models import CurrentWeatherHistory


class CurrentWeatherDAO(BaseDAO[CurrentWeatherHistory]):
    """
    Data Access Object (DAO) for weather history-related operations.
    This class provides methods to interact with the database for weather history management.
    """

    model = CurrentWeatherHistory
