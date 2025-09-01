from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.mixin import TimestampsMixin
from src.db.base import Base


class User(Base, TimestampsMixin):
    """Application user model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=1024), nullable=False)  # hashed
    # Optional profile data
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(15), nullable=True)

    # Access and activity flags
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
