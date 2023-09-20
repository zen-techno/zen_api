from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from src.models import Base

TestBase = declarative_base(metadata=Base.metadata)


class EntityReadSchema(BaseModel):
    id: UUID
    username: str
    balance: int


class Entity(TestBase):
    __tablename__ = "entity"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    balance: Mapped[int] = mapped_column(nullable=False)

    def to_read_model(self) -> EntityReadSchema:
        return EntityReadSchema(
            id=self.id, username=self.username, balance=self.balance
        )
