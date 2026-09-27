from typing import Any
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class RegisterRequest(BaseModel):

    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=120,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class UserOut(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    email: EmailStr
    full_name: str


class HomeItem(BaseModel):

    category: str = Field(
        min_length=2,
        max_length=100,
    )

    quantity: int = Field(
        default=1,
        ge=1,
        le=50,
    )


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=100_000_000,
    )

    room_type: str = Field(
        min_length=2,
        max_length=80,
    )

    style: str = Field(
        default="modern",
        max_length=80,
    )

    items: list[HomeItem] = Field(
        min_length=1,
        max_length=30,
    )

    city: str = Field(
        default="",
        max_length=80,
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=100_000_000,
    )

    guests: int = Field(
        gt=0,
        le=100_000,
    )

    event_type: str = Field(
        min_length=2,
        max_length=80,
    )

    venue: str = Field(
        default="flexible",
        max_length=120,
    )

    city: str = Field(
        default="",
        max_length=80,
    )

    food_preference: str = Field(
        default="mixed",
        max_length=120,
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=100_000_000,
    )

    occasion: str = Field(
        min_length=2,
        max_length=100,
    )

    style: str = Field(
        default="elegant",
        max_length=100,
    )

    outfit_description: str = Field(
        default="",
        max_length=500,
    )

    metal_preference: str = Field(
        default="any",
        max_length=80,
    )


class RecommendationItem(BaseModel):

    title: str

    category: str

    platform: str

    estimated_price: float = Field(
        ge=0
    )

    reason: str

    url: str

    confidence: float = Field(
        ge=0,
        le=1,
    )


class BudgetAllocation(BaseModel):

    category: str

    amount: float = Field(
        ge=0
    )

    percentage: float = Field(
        ge=0,
        le=100,
    )


class RecommendationResponse(BaseModel):

    planner_type: Literal[
        "home",
        "party",
        "jewelry",
    ]

    budget: float

    total_estimated: float

    within_budget: bool

    summary: str

    budget_allocation: list[BudgetAllocation]

    recommendations: list[RecommendationItem]

    tips: list[str] = []


class HistoryItem(BaseModel):

    id: int

    planner_type: str

    created_at: str

    response: dict[str, Any]