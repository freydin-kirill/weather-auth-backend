from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError

from src.db.session import async_session_factory


class BaseDAO[T]:
    """Base class for data access objects."""

    model: type[T]

    @classmethod
    async def find_all(cls, **filter_by) -> list[T]:
        """Return a list of records matching provided criteria.

        :param filter_by: filtering parameters, dict
        :returns: list of found objects, list[T]
        """

        async with async_session_factory() as session:
            # Build query with filtering parameters
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> T | None:
        """Find a single record by criteria or return None.

        :param filter_by: filtering parameters, dict
        :returns: found object or None, T | None
        """

        async with async_session_factory() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int) -> T | None:
        """Retrieve a record by its identifier.

        :param data_id: record identifier, int
        :returns: found object or None, T | None
        """

        return await cls.find_one_or_none(id=data_id)

    @classmethod
    async def create(cls, **values) -> dict:
        """Create a new record in the database.

        :param values: fields of the new record, dict
        :returns: success message and created object, dict
        """

        async with async_session_factory() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return {"message": "Create successful", "body": new_instance}

    @classmethod
    async def update(cls, item_id, **values) -> dict:
        """Update a record by its identifier.

        :param item_id: record identifier, int
        :param values: fields to update, dict
        :returns: success message, dict
        """

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
        """Remove a record from the database.

        :param item_id: record identifier, int
        :returns: success message, dict
        """

        async with async_session_factory() as session:
            query = delete(cls.model).filter(cls.model.id == item_id)
            await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return {"message": "Delete successful"}
