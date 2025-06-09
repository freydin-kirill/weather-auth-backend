from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('UTC', NOW())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('UTC', NOW())"),
        onupdate=datetime.now(UTC),
    )
