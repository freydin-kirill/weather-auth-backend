from datetime import UTC, datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.config import settings


engine = create_async_engine(url=settings.db_url_async)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    __repr_cols_number__ = 3
    __repr_cols_name__ = ()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.__repr_cols_name__ or idx < self.__repr_cols_number__:
                cols.append(f"{col}: {getattr(self, col)}")
        return f"\n<{self.__class__.__name__}> {', '.join(cols)}"

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('UTC', NOW())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('UTC', NOW())"), onupdate=datetime.now(UTC),
    )


if __name__ == "__main__":
    # Test the connection
    async def main():
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT VERSION()"))
            print(result.all())
    import asyncio
    asyncio.run(main())
