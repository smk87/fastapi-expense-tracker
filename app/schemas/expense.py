from datetime import datetime

from pydantic import BaseModel, Field


class ExpenseCreateDto(BaseModel):
    title: str = Field(
        ...,
        description="The title of the expense",
        min_length=3,
        max_length=50,
        examples=["Groceries"],
    )

    amount: float = Field(..., description="The amount of the expense", examples=[50.0])

    description: str = Field(
        ...,
        description="The description of the expense",
        max_length=500,
        examples=["Bought groceries"],
    )

    show: bool = Field(
        default=True, description="Whether to show the expense", examples=[True]
    )


class ExpenseResponseDto(BaseModel):
    id: int = Field(..., description="The ID of the expense", examples=[1])

    title: str = Field(
        ..., description="The title of the expense", examples=["Groceries"]
    )

    amount: float = Field(..., description="The amount of the expense", examples=[50.0])

    description: str = Field(
        ..., description="The description of the expense", examples=["Bought groceries"]
    )

    show: bool = Field(..., description="Whether to show the expense", examples=[True])

    created_at: datetime | str = Field(
        ..., description="The creation date of the expense", examples=["2022-01-01"]
    )

    model_config = {"from_attributes": True}


class ExpenseUpdateDto(BaseModel):
    title: str | None = Field(
        default=None,
        description="The title of the expense",
        min_length=3,
        max_length=50,
        examples=["Groceries"],
    )
    amount: float | None = Field(
        default=None, description="The amount of the expense", examples=[50.0]
    )
    description: str | None = Field(
        default=None,
        description="The description of the expense",
        max_length=500,
        examples=["Bought groceries"],
    )
    show: bool | None = Field(
        default=True, description="Whether to show the expense", examples=[True]
    )
