from typing import List, Optional

from sqlalchemy import delete, insert, select, update

from backend.src.core.repository.repository import (
    ID,
    AbstractRepository,
    DataDict,
    ReadSchema,
)
from backend.src.database.database import async_session_maker
from backend.src.models import Base


class SQLAlchemyRepository(AbstractRepository):
    model: Base = None
    session_maker = async_session_maker

    async def add_one(self, *, data: DataDict) -> ReadSchema:
        async with self.session_maker() as session:
            query = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one().to_read_model()

    async def get_all(self) -> List[ReadSchema]:
        async with self.session_maker() as session:
            query = select(self.model)
            result = await session.execute(query)
            return [item.to_read_model() for item in result.scalars()]

    async def get_one(self, **filter_by) -> Optional[ReadSchema]:
        async with self.session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            if result := result.scalar_one_or_none():
                return result.to_read_model()
            return None

    async def update_one(self, *, id: ID, data: DataDict) -> ReadSchema:
        async with self.session_maker() as session:
            query = (
                update(self.model)
                .values(**data)
                .filter_by(id=id)
                .returning(self.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one().to_read_model()

    async def delete_one(self, *, id: ID) -> None:
        async with self.session_maker() as session:
            query = delete(self.model).filter_by(id=id)
            await session.execute(query)
            await session.commit()