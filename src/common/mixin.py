from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('UTC', NOW())"),
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('UTC', NOW())"),
        onupdate=datetime.now(UTC),
    )


class TimestampsMixin(CreatedAtMixin, UpdatedAtMixin):
    pass
