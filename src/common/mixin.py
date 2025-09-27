from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    """Mixin adding record creation time."""

    # Creation time automatically set in UTC
    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('UTC', NOW())"),
    )


class UpdatedAtMixin:
    """Mixin adding last update time."""

    # Field updates on every record modification
    updated_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('UTC', NOW())"),
        onupdate=datetime.now(UTC),
    )


class TimestampsMixin(CreatedAtMixin, UpdatedAtMixin):
    """Combined mixin with creation and update timestamps."""

    pass
