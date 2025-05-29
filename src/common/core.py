from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session_factory


class BaseDAO:
    """
    Base Data Access Object (DAO) class.
    This class serves as a common for all DAO classes, providing common functionality.
    """

    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_factory() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        return await cls.find_one_or_none(id=data_id)

    @classmethod
    async def add(cls, **values):
        async with async_session_factory() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def update(cls, filter_by: dict, **values):
        pass
