from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, PositiveInt


class ExpenseReadSchema(BaseModel):
    id: UUID
    name: str
    amount: PositiveInt
    transaction_date: datetime
    who_paid_id: UUID
    category_id: UUID


class ExpenseCreateSchema(BaseModel):
    name: str
    amount: PositiveInt
    who_paid_id: UUID
    category_id: UUID


class ExpenseUpdateSchema(BaseModel):
    name: str
    amount: PositiveInt
    who_paid_id: UUID
    category_id: UUID
