from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings


engine = create_async_engine(url=settings.db_url_async)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


if __name__ == "__main__":
    # Test the connection
    async def main():
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT VERSION()"))
            print(result.all())

    import asyncio

    asyncio.run(main())
