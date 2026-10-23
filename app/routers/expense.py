from typing import Annotated

from core.db import get_db
from core.secure import get_current_user
from fastapi import APIRouter, Depends, Response, status
from models.expense import Expense
from models.user import User
from schemas.api_response import APIResponse
from schemas.expense import ExpenseCreateDto, ExpenseResponseDto, ExpenseUpdateDto
from sqlalchemy.orm import Session

expense_router = APIRouter(prefix="/expenses", tags=["Expense"])


# Create expense
@expense_router.post("/", response_model=APIResponse[ExpenseResponseDto])
def create_expense(
    expense_request_dto: ExpenseCreateDto,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    new_expense = Expense(
        title=expense_request_dto.title,
        amount=expense_request_dto.amount,
        description=expense_request_dto.description,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return APIResponse[ExpenseResponseDto](
        status="success",
        message="Expense created successfully",
        data=new_expense,
    )


# Get all expenses
@expense_router.get("/", response_model=APIResponse[list[ExpenseResponseDto]])
def get_expenses(db: Annotated[Session, Depends(get_db)]):
    expenses = db.query(Expense).all()

    return APIResponse[list[ExpenseResponseDto]](
        status="success", message="Expenses fetched successfully", data=expenses
    )


# Search expense by title
@expense_router.get("/search", response_model=APIResponse[list[ExpenseResponseDto]])
def search_expense(title: str, db: Annotated[Session, Depends(get_db)]):
    expenses = db.query(Expense).filter(Expense.title.ilike(f"%{title}%")).all()

    return APIResponse[list[ExpenseResponseDto]](
        status="success", message="Expenses fetched successfully", data=expenses
    )


# Get expense by id
@expense_router.get("/{id}", response_model=APIResponse[ExpenseResponseDto])
def get_expense(id: int, db: Annotated[Session, Depends(get_db)], response: Response):
    expense = db.get(Expense, id)

    if not expense:
        response.status_code = status.HTTP_404_NOT_FOUND

        return APIResponse[ExpenseResponseDto](
            status="failed",
            message="Expense doesn't exist",
        )

    return APIResponse[ExpenseResponseDto](
        status="success",
        message="Expense fetched successfully",
        data=expense,
    )


# Update expense by id
@expense_router.put("/{id}", response_model=APIResponse[ExpenseResponseDto])
def update_expense(
    id: int,
    expense_update_dto: ExpenseUpdateDto,
    db: Annotated[Session, Depends(get_db)],
    response: Response,
):
    expense = db.get(Expense, id)

    if not expense:
        response.status_code = status.HTTP_404_NOT_FOUND

        return APIResponse[ExpenseResponseDto](
            status="failed",
            message="Expense doesn't exist",
        )

    if expense_update_dto.title is not None:
        expense.title = expense_update_dto.title

    if expense_update_dto.amount is not None:
        expense.amount = expense_update_dto.amount

    if expense_update_dto.description is not None:
        expense.description = expense_update_dto.description

    if expense_update_dto.show is not None:
        expense.show = expense_update_dto.show

    db.commit()

    db.refresh(expense)

    return APIResponse[ExpenseResponseDto](
        status="success",
        message="Expense updated successfully",
        data=expense,
    )


# Delete expense by id
@expense_router.delete("/{id}", response_model=APIResponse[ExpenseResponseDto])
def delete_expense(
    id: int, db: Annotated[Session, Depends(get_db)], response: Response
):
    expense = db.get(Expense, id)

    if not expense:
        response.status_code = status.HTTP_404_NOT_FOUND

        return APIResponse[ExpenseResponseDto](
            status="failed",
            message="Expense doesn't exist",
        )

    db.delete(expense)
    db.commit()

    return APIResponse[ExpenseResponseDto](
        status="success",
        message="Expense deleted successfully",
    )
