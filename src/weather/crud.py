from src.common.crud import BaseDAO
from src.weather.models import WeatherSearch
from src.weather.providers import get_write_schema_by_provider
from src.weather.utils import ProviderEnum


class WeatherSearchDAO(BaseDAO[WeatherSearch]):
    """
    Data Access Object (DAO) for weather history-related operations.
    This class provides methods to interact with the database for weather history management.
    """

    model = WeatherSearch

    @classmethod
    async def log_weather_search(cls, user_id: int, provider: ProviderEnum, data: dict) -> dict:
        log_data = {"user_id": user_id, "provider": provider.value}
        log_data.update(data)
        record = get_write_schema_by_provider(provider).model_validate(log_data)
        record_dict = record.model_dump()
        return await cls.create(**record_dict)
