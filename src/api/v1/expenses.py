from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import (
    ExpenseServiceDepends,
    valid_expense_id,
    valid_expense_schema,
)
from src.schemas.expenses import (
    ExpenseCreateSchema,
    ExpenseReadSchema,
    ExpenseUpdateSchema,
)

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get(
    "", response_model=list[ExpenseReadSchema], status_code=status.HTTP_200_OK
)
async def get_expenses(
    expense_service: ExpenseServiceDepends,
) -> list[ExpenseReadSchema]:
    return await expense_service.get_all_expenses()


@router.get(
    "/{expense_id}",
    response_model=ExpenseReadSchema,
    status_code=status.HTTP_200_OK,
)
def get_expense_by_id(
    valid_expense: ExpenseReadSchema = Depends(valid_expense_id),
) -> ExpenseReadSchema:
    return valid_expense


@router.post(
    "", response_model=ExpenseReadSchema, status_code=status.HTTP_201_CREATED
)
async def add_expense(
    expense_service: ExpenseServiceDepends,
    valid_expense: ExpenseCreateSchema = Depends(valid_expense_schema),
) -> ExpenseReadSchema:
    return await expense_service.create_expense(expense=valid_expense)


@router.put(
    "/{expense_id}",
    response_model=ExpenseReadSchema,
    dependencies=[Depends(valid_expense_id)],
    status_code=status.HTTP_200_OK,
)
async def update_expense_by_id(
    expense_id: UUID,
    expense_service: ExpenseServiceDepends,
    valid_expense: ExpenseUpdateSchema = Depends(valid_expense_schema),
) -> ExpenseReadSchema:
    return await expense_service.update_expense_by_id(
        id=expense_id, expense=valid_expense
    )


@router.delete(
    "/{expense_id}",
    response_model=None,
    dependencies=[Depends(valid_expense_id)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_expense_by_uuid(
    expense_id: UUID, expense_service: ExpenseServiceDepends
) -> None:
    await expense_service.delete_expense_by_id(id=expense_id)
