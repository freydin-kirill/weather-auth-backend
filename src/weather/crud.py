from src.common.crud import BaseDAO
from src.weather.adapters.base import BaseWeatherAdapter
from src.weather.models import WeatherSearch


class WeatherSearchDAO(BaseDAO[WeatherSearch]):
    """
    Data Access Object (DAO) for weather history-related operations.
    This class provides methods to interact with the database for weather history management.
    """

    model = WeatherSearch

    @classmethod
    async def log_weather_search(cls, user_id: int, adapter: BaseWeatherAdapter, raw_response: dict) -> dict:
        record = raw_response.copy()
        record.update({"user_id": user_id, "provider": adapter.name()})
        record = adapter.get_write_schema().model_validate(record)
        return await cls.create(**record.model_dump())
