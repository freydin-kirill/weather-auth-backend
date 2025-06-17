from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


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
