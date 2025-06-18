from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.mixin import CreatedAtMixin
from src.db.base import Base
from src.weather.enums import Providers


class WeatherSearch(Base, CreatedAtMixin):
    __tablename__ = "weather_searches"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    provider: Mapped[Providers] = mapped_column(nullable=False)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)
