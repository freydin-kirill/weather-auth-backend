from typing import Generic, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError

from src.db.base import Base
from src.db.session import async_session_factory


T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    """
    Base Data Access Object (DAO) class.
    This class serves as a common for all DAO classes, providing common functionality.
    """

    model = type[T]

    @classmethod
    async def find_all(cls):
        async with async_session_factory() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

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
    async def create(cls, **values) -> dict:
        async with async_session_factory() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return {"message": "Update successful", "body": new_instance}

    @classmethod
    async def update(cls, item_id, **values) -> dict:
        async with async_session_factory() as session:
            query = update(cls.model).filter(cls.model.id == item_id).values(**values)
            await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return {"message": "Update successful"}

    @classmethod
    async def delete(cls, item_id) -> dict:
        async with async_session_factory() as session:
            query = delete(cls.model).filter(cls.model.id == item_id)
            await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return {"message": "Delete successful"}
