from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.common.mixin import CreatedAtMixin
from src.db.base import Base


class CurrentWeatherHistory(Base, CreatedAtMixin):
    __tablename__ = "current_weather_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    timezone: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    wind_speed: Mapped[float] = mapped_column(nullable=False)
    time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)


class WeatherProvider(Base):
    __tablename__ = "weather_provider"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    params: Mapped[dict] = mapped_column(JSON, nullable=False)
    api_url: Mapped[str] = mapped_column(nullable=False)
    api_key: Mapped[str | None] = mapped_column(nullable=True)
    enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
